# CarbonScanner

## Overview

CarbonScanner is an innovative application designed to analyze and track carbon footprints through advanced AI technologies. The project aims to provide users with insights about environmental impacts and promote sustainable practices.

## Features

- **Image Analysis**: Upload and analyze images to detect carbon-related data
- **AI-Powered Insights**: Leverages Gemini AI and LangChain for intelligent processing of environmental data
- **User Authentication**: Secure account management and personalized experiences
- **Data Visualization**: Track and visualize carbon metrics over time
- **Food Production Impact Analysis**: Analyze carbon footprint of food production systems

## Project Structure

```text
├── backend/             # Python-based backend services
│   ├── carbon_scanner/  # Core application code
│   │   ├── app.py       # Main application entry point
│   │   ├── authentication/  # Authentication services
│   │   ├── database/    # Database connectivity and models
│   │   ├── genai/       # AI processing components
│   │   └── images/      # Image handling and processing
│   └── tests/           # Backend unit tests
├── frontend/            # React-based frontend (Vite)
│   ├── public/          # Static assets
│   └── src/             # Frontend source code
└── documentation/       # Project documentation
```

## Technologies

- **Backend**: Python 3.10.12, Flask/FastAPI
- **Frontend**: React, Vite
- **AI/ML**: Gemini AI, LangChain
- **Database**: SQL/NoSQL database (based on db_manager implementation)
- **Authentication**: JWT-based authentication

## Getting Started

### Prerequisites

- Python 3.10.12
- Node.js and npm
- Required API keys for AI services

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
# Configure your .env file based on .env.example
python -m carbon_scanner.app
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Usage

- Register an account to access full functionality
- Upload images for carbon footprint analysis
- View personalized recommendations for reducing environmental impact
- Track your progress over time

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
