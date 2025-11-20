"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# moviQ specific schemas (used by the app)

class Lead(BaseModel):
    """
    Leads from contact form
    Collection name: "lead"
    """
    full_name: str = Field(..., description="Applicant full name")
    phone: str = Field(..., description="Phone number")
    email: EmailStr = Field(..., description="Email address")
    app: Literal['Uber','Bolt','FreeNow','Inna'] = Field(..., description="TNC app they drive with")
    preferred_model: Optional[str] = Field(None, description="Preferred car model")

class Vehicle(BaseModel):
    """
    Vehicles available in the fleet
    Collection name: "vehicle"
    """
    make: str
    model: str
    variant: Optional[str] = None
    price_monthly: int = Field(..., description="Gross monthly rate in PLN")
    fuel: Literal['benzyna','diesel','hybryda','elektryczny','LPG']
    photo_url: Optional[str] = None

class PricingPlan(BaseModel):
    """
    Pricing plans for website display
    Collection name: "pricingplan"
    """
    name: Literal['Standard','Comfort','Premium']
    price_from: int = Field(..., description="Starting gross price per month in PLN")
    includes: list[str] = Field(default_factory=list)

class FAQItem(BaseModel):
    """
    Frequently asked questions
    Collection name: "faqitem"
    """
    question: str
    answer: str

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
