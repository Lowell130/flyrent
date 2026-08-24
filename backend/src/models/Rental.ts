import { Schema, model, Document } from 'mongoose';

export type Platform = 'Facebook' | 'Subito' | 'Idealista' | 'Immobiliare' | 'Privato' | 'Altro';
export type UtilitiesType = 'Incluse' | 'Forfait' | 'A consumo';
export type StatusType = 'Bozza' | 'Contattato' | 'In Attesa' | 'Visita/Videochiamata' | 'Opzionato' | 'Scartato' | 'Confermato';
export type WifiType = 'Fibra FTTH' | 'FTTC' | 'FWA' | 'Wi-Fi da verificare' | 'Assente';
export type WorkspaceType = 'Scrivania dedicata' | 'Tavolo grande' | 'Nessuna';

export interface IRental extends Document {
  title: string;
  url?: string;
  platform: Platform;
  city: string;
  address?: string;
  monthlyPrice: number;
  utilities: UtilitiesType;
  utilitiesPriceEstimate: number;
  deposit: number;
  status: StatusType;
  wifiType: WifiType;
  workspaceType: WorkspaceType;
  availablePeriod?: string;
  contactName?: string;
  contactPhone?: string;
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
}

const RentalSchema = new Schema<IRental>(
  {
    title: { type: String, required: true, trim: true },
    url: { type: String, trim: true },
    platform: {
      type: String,
      enum: ['Facebook', 'Subito', 'Idealista', 'Immobiliare', 'Privato', 'Altro'],
      default: 'Facebook'
    },
    city: { type: String, required: true, trim: true },
    address: { type: String, trim: true },
    monthlyPrice: { type: Number, required: true, min: 0 },
    utilities: {
      type: String,
      enum: ['Incluse', 'Forfait', 'A consumo'],
      default: 'A consumo'
    },
    utilitiesPriceEstimate: { type: Number, default: 0 },
    deposit: { type: Number, default: 0 },
    status: {
      type: String,
      enum: ['Bozza', 'Contattato', 'In Attesa', 'Visita/Videochiamata', 'Opzionato', 'Scartato', 'Confermato'],
      default: 'Bozza'
    },
    wifiType: {
      type: String,
      enum: ['Fibra FTTH', 'FTTC', 'FWA', 'Wi-Fi da verificare', 'Assente'],
      default: 'Wi-Fi da verificare'
    },
    workspaceType: {
      type: String,
      enum: ['Scrivania dedicata', 'Tavolo grande', 'Nessuna'],
      default: 'Tavolo grande'
    },
    availablePeriod: { type: String, trim: true },
    contactName: { type: String, trim: true },
    contactPhone: { type: String, trim: true },
    notes: { type: String, trim: true }
  },
  {
    timestamps: true
  }
);

export const Rental = model<IRental>('Rental', RentalSchema);
