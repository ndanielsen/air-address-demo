import air
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated, List
import json

app = air.Air()
api = FastAPI()

# Air's JinjaRenderer is a shortcut for using Jinja templates
jinja = air.JinjaRenderer(directory="templates")

# In-memory storage for addresses (in production, use a database)
addresses_db: List[dict] = []

# Define the Address model using Pydantic
class AddressModel(BaseModel):
    street_address: str = air.AirField(min_length=1, label="Street Address")
    city: str = air.AirField(min_length=1, label="City")
    state: str = air.AirField(min_length=1, label="State/Province")
    postal_code: str = air.AirField(min_length=1, label="ZIP/Postal Code")
    country: str = air.AirField(min_length=1, default="USA", label="Country")

# Create the AirForm class for the address form
class AddressForm(air.AirForm):
    model = AddressModel

# Navigation component
def navigation():
    return air.Nav(
        air.Ul(
            air.Li(air.A("Home", href="/")),
            air.Li(air.A("Address Form", href="/address")),
            air.Li(air.A("Address List", href="/addresses")),
            air.Li(air.A("API", href="/api")),
        )
    )

# Base layout component
def base_layout(title: str, *content):
    return air.layouts.picocss(
        air.Title(title),
        navigation(),
        *content,
        air.Footer(
            air.P(
                "Built with ",
                air.A("Air Framework", href="https://github.com/air-framework/air"),
                " | ",
                air.A("API Documentation", href="/api/docs"),
            ),
            style="text-align: center; margin-top: 2rem;"
        )
    )

@app.get("/")
def index(request: air.requests.Request):
    return base_layout(
        "Air Demo - Home",
        air.Header(
            air.H1("Welcome to Air Demo"),
            air.P("A demonstration of the Air web framework with FastAPI integration."),
        ),
        air.Section(
            air.H2("Features"),
            air.Ul(
                air.Li("Address management with form validation"),
                air.Li("HTMX-powered dynamic updates"),
                air.Li("Built-in API with FastAPI"),
                air.Li("Clean UI with PicoCSS"),
            ),
        ),
        air.Section(
            air.H2("Quick Links"),
            air.Article(
                air.A("Add New Address", href="/address", role="button"),
                air.A("View All Addresses", href="/addresses", role="button", style="margin-left: 1rem;"),
            ),
        ),
    )

@app.get("/address")
def address_form_page(request: air.requests.Request):
    form = AddressForm()
    return base_layout(
        "Add Address",
        air.H1("Address Form"),
        air.Form(
            form.render(),
            air.Button("Submit", type="submit"),
            method="post",
            action="/address",
            hx_post="/address",
            hx_target="#form-container",
            hx_swap="innerHTML",
            id="form-container"
        ),
    )

@app.post("/address")
async def submit_address(request: air.requests.Request, address: Annotated[AddressForm, Depends(AddressForm.from_request)]):
    if address.is_valid:
        # Store the address
        address_data = address.data.model_dump()
        address_data['id'] = len(addresses_db) + 1
        addresses_db.append(address_data)
        
        # Return success message with HTMX
        return air.Div(
            air.Article(
                air.Header(air.H3("✅ Address Submitted Successfully!")),
                air.P(
                    f"Added address for {address.data.street_address}, {address.data.city}"
                ),
                air.A("Add Another Address", href="/address", role="button"),
                air.A("View All Addresses", href="/addresses", role="button", style="margin-left: 1rem;"),
            ),
            id="form-container"
        )
    else:
        # Re-render form with errors
        return air.Div(
            air.Article(
                air.Header(air.Strong("Please correct the errors below:")),
                air.Ul(*[air.Li(f"{error['loc'][0]}: {error['msg']}") for error in address.errors]),
                style="background: var(--error-bg); border-color: var(--error);"
            ),
            air.Form(
                address.render(),
                air.Button("Submit", type="submit"),
                method="post",
                action="/address",
                hx_post="/address",
                hx_target="#form-container",
                hx_swap="innerHTML",
            ),
            id="form-container"
        )

@app.get("/addresses")
def address_list(request: air.requests.Request):
    if not addresses_db:
        content = air.P("No addresses have been added yet.", style="text-align: center;")
    else:
        rows = []
        for addr in addresses_db:
            rows.append(
                air.Tr(
                    air.Td(str(addr['id'])),
                    air.Td(addr['street_address']),
                    air.Td(addr['city']),
                    air.Td(addr['state']),
                    air.Td(addr['postal_code']),
                    air.Td(addr['country']),
                    air.Td(
                        air.Button(
                            "Delete",
                            hx_delete=f"/address/{addr['id']}",
                            hx_target=f"#row-{addr['id']}",
                            hx_swap="outerHTML",
                            hx_confirm="Are you sure you want to delete this address?",
                            style="padding: 0.25rem 0.5rem; font-size: 0.875rem;",
                        )
                    ),
                    id=f"row-{addr['id']}"
                )
            )
        
        content = air.Div(
            air.Input(
                type="search",
                placeholder="Search addresses...",
                hx_post="/search-addresses",
                hx_trigger="input changed delay:500ms",
                hx_target="#address-table-body",
                style="margin-bottom: 1rem;"
            ),
            air.Table(
                air.Thead(
                    air.Tr(
                        air.Th("ID"),
                        air.Th("Street"),
                        air.Th("City"),
                        air.Th("State"),
                        air.Th("ZIP"),
                        air.Th("Country"),
                        air.Th("Actions"),
                    )
                ),
                air.Tbody(*rows, id="address-table-body"),
            ),
        )
    
    return base_layout(
        "Address List",
        air.H1("Saved Addresses"),
        content,
        air.Div(
            air.A("Add New Address", href="/address", role="button"),
            air.A("Export as JSON", href="/api/addresses", role="button", style="margin-left: 1rem;"),
            style="margin-top: 2rem;"
        ),
    )

@app.delete("/address/{address_id}")
def delete_address(address_id: int):
    global addresses_db
    addresses_db = [addr for addr in addresses_db if addr['id'] != address_id]
    return ""  # Return empty string for HTMX to remove the row

@app.post("/search-addresses")
async def search_addresses(request: air.requests.Request):
    form_data = await request.form()
    search_term = form_data.get("search", "").lower()
    
    filtered_addresses = [
        addr for addr in addresses_db
        if search_term in addr['street_address'].lower()
        or search_term in addr['city'].lower()
        or search_term in addr['state'].lower()
        or search_term in addr['postal_code'].lower()
        or search_term in addr['country'].lower()
    ]
    
    if not filtered_addresses:
        return air.Tr(air.Td("No addresses found", colspan="7", style="text-align: center;"))
    
    rows = []
    for addr in filtered_addresses:
        rows.append(
            air.Tr(
                air.Td(str(addr['id'])),
                air.Td(addr['street_address']),
                air.Td(addr['city']),
                air.Td(addr['state']),
                air.Td(addr['postal_code']),
                air.Td(addr['country']),
                air.Td(
                    air.Button(
                        "Delete",
                        hx_delete=f"/address/{addr['id']}",
                        hx_target=f"#row-{addr['id']}",
                        hx_swap="outerHTML",
                        hx_confirm="Are you sure you want to delete this address?",
                        style="padding: 0.25rem 0.5rem; font-size: 0.875rem;",
                    )
                ),
                id=f"row-{addr['id']}"
            )
        )
    
    return air.Raw("".join(str(row) for row in rows))

# API endpoints
@api.get("/")
def api_root():
    return {"message": "Awesome SaaS is powered by FastAPI"}

@api.get("/addresses")
def api_get_addresses():
    return {"addresses": addresses_db, "count": len(addresses_db)}

@api.post("/addresses")
def api_create_address(address: AddressModel):
    address_data = address.model_dump()
    address_data['id'] = len(addresses_db) + 1
    addresses_db.append(address_data)
    return {"message": "Address created", "address": address_data}

# Combining the Air and and FastAPI apps into one
app.mount("/api", api)
