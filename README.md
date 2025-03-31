

![Logo](https://github.com/gxnca/Lukrium/blob/main/frontend/public/images/lukrium.png?raw=true)
# Lukrium 

Lukrium is an internal tool developed for MC Sonae to optimize price management. It includes a price optimization generator for new products, comparing them with market prices, and a price review alert system that identifies products losing competitiveness. With this solution, the company can quickly adapt to the market, ensuring strategic and competitive pricing.


## Getting Started

### Frontend

#### Navigate to the frontend directory:

```bash
  cd /frontend
```

#### Install dependencies:

```bash
  bun install
```

#### Start the development server:

```bash
  bun dev
```

### Backend

#### Navigate to the backend directory:

```bash
  cd /backend/src
```

#### Install dependencies:

```bash
  pip install -r requirements.txt
```

#### Database Setup:

Create a folder named `data` and place the dataset files provided by Sonae inside it.
Then, run the following command to build the database files:
```bash
  python introduz.py
```

#### Start the API:
```bash
  python main.py
```



## Environment Variables

To run this project, you need to create a .env file and define the following environment variable:

`API_KEY=your_gemini_ai_api_key`



## Tech Stack

**Front-end:** Next.js, Tailwind CSS

**Back-end:** Pyhton, FastApi

