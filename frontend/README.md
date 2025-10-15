# Quantum Image Retrieval - Frontend

React TypeScript frontend for the Quantum Image Retrieval System.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Material-UI** - Component library
- **Axios** - HTTP client
- **Appwrite SDK** - Backend integration

## 📁 Project Structure

```
src/
├── main.tsx              # Entry point
├── App.tsx               # Main app component
├── components/           # React components
│   ├── ImageUpload.tsx   # Upload with drag & drop
│   ├── ImageCard.tsx     # Image result card
│   ├── SearchResults.tsx # Results display
│   └── StatsPanel.tsx    # Statistics dashboard
├── services/             # API & services
│   ├── api.ts           # Backend API client
│   └── appwrite.ts      # Appwrite SDK setup
└── types/               # TypeScript definitions
    └── index.ts         # Type interfaces
```

## 🔧 Configuration

Environment variables in `.env`:

```env
VITE_APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
VITE_APPWRITE_PROJECT_ID=68eed0ee0033a7ceca80
VITE_API_URL=http://localhost:8000
```

## 🎨 Features

- Drag & drop image upload
- Real-time similarity search
- Material Design dark theme
- Responsive layout
- Image preview modal
- Statistics dashboard
- Type-safe development

## 🌐 Development

Runs on: http://localhost:5173

API proxy configured to forward `/api` requests to backend on port 8000.

## 📦 Build

```bash
npm run build
```

Output in `dist/` directory, ready for deployment to:
- Vercel
- Netlify
- AWS Amplify
- Any static hosting
