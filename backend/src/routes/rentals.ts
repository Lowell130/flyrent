import { Router, Request, Response } from 'express';
import { Rental } from '../models/Rental';

const router = Router();

// GET /api/rentals - List rentals with optional filtering
router.get('/', async (req: Request, res: Response) => {
  try {
    const { status, city, wifiType, search } = req.query;
    const filter: any = {};

    if (status) filter.status = status;
    if (city) filter.city = new RegExp(String(city), 'i');
    if (wifiType) filter.wifiType = wifiType;
    if (search) {
      const searchRegex = new RegExp(String(search), 'i');
      filter.$or = [
        { title: searchRegex },
        { city: searchRegex },
        { notes: searchRegex },
        { contactName: searchRegex }
      ];
    }

    const rentals = await Rental.find(filter).sort({ updatedAt: -1 });
    res.json(rentals);
  } catch (error: any) {
    res.status(500).json({ message: 'Errore nel recupero degli annunci', error: error.message });
  }
});

// GET /api/rentals/:id - Single rental
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const rental = await Rental.findById(req.params.id);
    if (!rental) {
      return res.status(404).json({ message: 'Annuncio non trovato' });
    }
    res.json(rental);
  } catch (error: any) {
    res.status(500).json({ message: 'Errore nel recupero dell\'annuncio', error: error.message });
  }
});

// POST /api/rentals - Create rental
router.post('/', async (req: Request, res: Response) => {
  try {
    const newRental = new Rental(req.body);
    const saved = await newRental.save();
    res.status(201).json(saved);
  } catch (error: any) {
    res.status(400).json({ message: 'Errore nella creazione dell\'annuncio', error: error.message });
  }
});

// PUT /api/rentals/:id - Update rental
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const updated = await Rental.findByIdAndUpdate(req.params.id, req.body, { new: true, runValidators: true });
    if (!updated) {
      return res.status(404).json({ message: 'Annuncio non trovato' });
    }
    res.json(updated);
  } catch (error: any) {
    res.status(400).json({ message: 'Errore nell\'aggiornamento dell\'annuncio', error: error.message });
  }
});

// DELETE /api/rentals/:id - Delete rental
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const deleted = await Rental.findByIdAndDelete(req.params.id);
    if (!deleted) {
      return res.status(404).json({ message: 'Annuncio non trovato' });
    }
    res.json({ message: 'Annuncio eliminato con successo', id: req.params.id });
  } catch (error: any) {
    res.status(500).json({ message: 'Errore nell\'eliminazione dell\'annuncio', error: error.message });
  }
});

// POST /api/rentals/seed - Seed sample data for testing
router.post('/seed', async (req: Request, res: Response) => {
  try {
    const count = await Rental.countDocuments();
    if (count > 0) {
      return res.json({ message: 'Database già popolato', count });
    }

    const sampleData = [
      {
        title: 'Bilocale Vista Mare vicino Stazione',
        url: 'https://www.subito.it/appartamenti/bilocale-termoli',
        platform: 'Subito',
        city: 'Termoli',
        address: 'Via XXIV Maggio, Termoli',
        monthlyPrice: 550,
        utilities: 'Incluse',
        utilitiesPriceEstimate: 0,
        deposit: 550,
        status: 'Contattato',
        wifiType: 'Fibra FTTH',
        workspaceType: 'Scrivania dedicata',
        availablePeriod: 'Ottobre - Novembre (2 mesi)',
        contactName: 'Marco (Proprietario)',
        contactPhone: '+39 333 1234567',
        notes: 'Inviato messaggio WhatsApp il 22 Agosto. In attesa di risposta sulle spese condominiali.'
      },
      {
        title: 'Trilocale ristrutturato zona Porta Nuova',
        url: 'https://www.idealista.it/immobile/pescara-portanuova',
        platform: 'Idealista',
        city: 'Pescara',
        address: 'Viale Marconi, Pescara',
        monthlyPrice: 650,
        utilities: 'A consumo',
        utilitiesPriceEstimate: 100,
        deposit: 1300,
        status: 'In Attesa',
        wifiType: 'Fibra FTTH',
        workspaceType: 'Tavolo grande',
        availablePeriod: '15 Settembre - 15 Novembre',
        contactName: 'Agenzia Immobiliare Pescara',
        contactPhone: '+39 085 9876543',
        notes: 'Chiamato l\'agenzia, hanno confermato la fibra 1Gbps. Disponibile per videochiamata Giovedì.'
      },
      {
        title: 'Appartamento luminoso a 200m dalla spiaggia',
        url: 'https://www.facebook.com/marketplace/item/12345678',
        platform: 'Facebook',
        city: 'Termoli',
        address: 'Lungomare Cristoforo Colombo',
        monthlyPrice: 480,
        utilities: 'Forfait',
        utilitiesPriceEstimate: 50,
        deposit: 500,
        status: 'Visita/Videochiamata',
        wifiType: 'Wi-Fi da verificare',
        workspaceType: 'Scrivania dedicata',
        availablePeriod: 'Settembre - Ottobre',
        contactName: 'Lucia',
        contactPhone: '+39 347 1122334',
        notes: 'Fissata videochiamata per domani alle 18:00 per mostrare la postazione e fare lo speedtest.'
      },
      {
        title: 'Monolocale moderno zona Pescara Centro',
        url: 'https://www.immobiliare.it/annuncio-pescara-centro',
        platform: 'Immobiliare',
        city: 'Pescara',
        address: 'Corso Umberto I',
        monthlyPrice: 700,
        utilities: 'A consumo',
        utilitiesPriceEstimate: 80,
        deposit: 700,
        status: 'Bozza',
        wifiType: 'FTTC',
        workspaceType: 'Tavolo grande',
        availablePeriod: 'Da Ottobre',
        contactName: 'Giovanni',
        contactPhone: '',
        notes: 'Bozza salvata. Da verificare se affittano per soli 2 mesi.'
      }
    ];

    const inserted = await Rental.insertMany(sampleData);
    res.status(201).json({ message: 'Dati di esempio inseriti con successo', count: inserted.length, data: inserted });
  } catch (error: any) {
    res.status(500).json({ message: 'Errore nel seeding del database', error: error.message });
  }
});

export default router;
