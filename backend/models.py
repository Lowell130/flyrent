from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- Auth Models ---

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    role: str
    createdAt: Optional[datetime] = None

    class Config:
        populate_by_name = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# --- Rental Models ---

class RentalBase(BaseModel):
    title: str
    url: Optional[str] = ""
    platform: str = "Facebook"  # Facebook, Subito, Idealista, Immobiliare, Privato, Altro
    city: str
    address: Optional[str] = ""
    monthlyPrice: float
    utilities: str = "A consumo"  # Incluse, Forfait, A consumo
    utilitiesPriceEstimate: float = 0.0
    condoFees: str = "Escluse"  # Incluse, Escluse, Forfait
    condoFeesPriceEstimate: float = 0.0
    deposit: float = 0.0
    status: str = "Bozza"  # Bozza, Contattato, In Attesa, Visita/Videochiamata, Opzionato, Scartato, Confermato
    wifiType: str = "Wi-Fi da verificare"  # Fibra FTTH, FTTC, FWA, Wi-Fi da verificare, Assente
    workspaceType: str = "Tavolo grande"  # Scrivania dedicata, Tavolo grande, Nessuna
    parkingType: str = "Parcheggio libero in strada"  # Posto auto riservato, Box / Garage privato, Parcheggio libero in strada, Parcheggio a pagamento, Nessun parcheggio
    availablePeriod: Optional[str] = ""
    contactName: Optional[str] = ""
    contactPhone: Optional[str] = ""
    notes: Optional[str] = ""
    images: List[str] = []

class RentalCreate(RentalBase):
    pass

class RentalUpdate(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    platform: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    monthlyPrice: Optional[float] = None
    utilities: Optional[str] = None
    utilitiesPriceEstimate: Optional[float] = None
    condoFees: Optional[str] = None
    condoFeesPriceEstimate: Optional[float] = None
    deposit: Optional[float] = None
    status: Optional[str] = None
    wifiType: Optional[str] = None
    workspaceType: Optional[str] = None
    parkingType: Optional[str] = None
    availablePeriod: Optional[str] = None
    contactName: Optional[str] = None
    contactPhone: Optional[str] = None
    notes: Optional[str] = None
    images: Optional[List[str]] = None

class RentalResponse(RentalBase):
    id: str = Field(alias="_id")
    owner_id: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True
