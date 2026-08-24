export type Platform = 'Facebook' | 'Subito' | 'Idealista' | 'Immobiliare' | 'Privato' | 'Altro';
export type UtilitiesType = 'Incluse' | 'Forfait' | 'A consumo';
export type CondoFeesType = 'Incluse' | 'Escluse' | 'Forfait';
export type StatusType = 'Bozza' | 'Contattato' | 'In Attesa' | 'Visita/Videochiamata' | 'Opzionato' | 'Scartato' | 'Confermato';
export type WifiType = 'Fibra FTTH' | 'FTTC' | 'FWA' | 'Wi-Fi da verificare' | 'Assente';
export type WorkspaceType = 'Scrivania dedicata' | 'Tavolo grande' | 'Nessuna';
export type ParkingType = 'Posto auto riservato' | 'Box / Garage privato' | 'Parcheggio libero in strada' | 'Parcheggio a pagamento' | 'Nessun parcheggio';

export interface Rental {
  _id: string;
  title: string;
  url?: string;
  platform: Platform;
  city: string;
  address?: string;
  monthlyPrice: number;
  utilities: UtilitiesType;
  utilitiesPriceEstimate: number;
  condoFees: CondoFeesType;
  condoFeesPriceEstimate: number;
  deposit: number;
  status: StatusType;
  wifiType: WifiType;
  workspaceType: WorkspaceType;
  parkingType: ParkingType;
  ratingNeighborhood?: number;
  ratingServices?: number;
  ratingTransport?: number;
  availablePeriod?: string;
  contactName?: string;
  contactPhone?: string;
  notes?: string;
  images?: string[];
  createdAt?: string;
  updatedAt?: string;
}

export interface RentalFormData {
  title: string;
  url?: string;
  platform: Platform;
  city: string;
  address?: string;
  monthlyPrice: number;
  utilities: UtilitiesType;
  utilitiesPriceEstimate: number;
  condoFees: CondoFeesType;
  condoFeesPriceEstimate: number;
  deposit: number;
  status: StatusType;
  wifiType: WifiType;
  workspaceType: WorkspaceType;
  parkingType: ParkingType;
  ratingNeighborhood?: number;
  ratingServices?: number;
  ratingTransport?: number;
  availablePeriod?: string;
  contactName?: string;
  contactPhone?: string;
  notes?: string;
  images?: string[];
}
