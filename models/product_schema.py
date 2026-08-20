from typing import Optional, List
from pydantic import BaseModel, Field


class Specification(BaseModel):
    name: str = Field(description="Name of the specification")
    value: Optional[str] = Field(
        default=None,
        description="Value of the specification"
    )
    unit: Optional[str] = Field(
        default=None,
        description="Unit of measurement"
    )
    source_text: Optional[str] = Field(
        default=None,
        description="Exact sentence or phrase from the source supporting this value"
    )
    page: Optional[int] = Field(
        default=None,
        description="Page number where the information was found"
    )


class Product(BaseModel):
    product_name: str = Field(
        description="Name of the industrial product"
    )

    category: Optional[str] = Field(
        default=None,
        description="Product category"
    )

    manufacturer: Optional[str] = Field(
        default=None,
        description="Manufacturer or brand"
    )

    description: Optional[str] = Field(
        default=None,
        description="Short product description"
    )

    specifications: List[Specification] = Field(
        default_factory=list,
        description="List of technical specifications"
    )

    applications: List[str] = Field(
        default_factory=list,
        description="Known applications of the product"
    )

    industries: List[str] = Field(
        default_factory=list,
        description="Industries where the product is used"
    )