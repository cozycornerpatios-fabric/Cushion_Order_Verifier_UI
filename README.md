# Cushion Order Analyzer

A FastAPI web application that uses AI to automatically analyze customer conversations and extract cushion order details. The app can process both text input and audio files to identify specifications, pricing, and requirements without manual input.

## Features

- 🛋️ **Automatic Order Analysis**: AI-powered extraction of cushion order details
- 📝 **Text Input**: Paste customer conversations or chat text
- 🎵 **Audio Processing**: Upload audio files for transcription and analysis
- 🛍️ **Shopify Integration**: Fetch order details directly from your Shopify endpoint using Order ID
- ✏️ **Manual Input**: Traditional text input for orders from other sources
- 🎨 **Modern UI**: Beautiful, responsive web interface
- 🔒 **Secure**: Environment variable configuration for API keys
- 🤖 **Smart Analysis**: GPT automatically identifies specifications, pricing, and requirements

## Setup

### 1. **Activate the virtual environment:**
   ```bash
   # On Windows (Git Bash)
   source venv/Scripts/activate
   
   # On Windows (PowerShell)
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

### 2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Configure API Keys:**
   Create a `.env` file in the project root:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your-actual-openai-api-key" > .env
   ```
   
   **Get your OpenAI API key from:** https://platform.openai.com/api-keys

   **Shopify integration is already configured** with your endpoint in the code.

### 4. **Run the application:**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 5. **Access the application:**
   Open your browser and go to: http://localhost:8000

## Project Structure

```
Cushion_Order_Verifier_UI/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore file
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface template
├── static/               # Static files (CSS, JS, images)
└── venv/                 # Virtual environment (do not modify)
```

## Usage

1. **Choose Order Source**:
   - **Shopify**: Enter the Shopify Order ID to fetch order details from your endpoint
   - **Manual Input**: Paste order details from Zendesk, Etsy, or other sources

2. **Provide Customer Communication**: Either:
   - Paste chat text or conversation
   - Upload an audio file (MP3, WAV, etc.)
   - Or both for comprehensive analysis

3. **Click "Verify Order"**: The AI will automatically:
   - Extract cushion specifications (size, material, color, style)
   - Identify quantity and pricing
   - Find special requirements or customizations
   - Determine delivery preferences
   - Provide a comprehensive order summary
   - Compare order details with customer communication

4. **Review Results**: See the detailed analysis with order summary, specifications, and recommendations

## What the AI Analyzes

The application automatically extracts and identifies:
- **Cushion Specifications**: Size, material, color, style
- **Quantity**: Number of cushions ordered
- **Special Requirements**: Customizations, special instructions
- **Pricing Information**: Costs, discounts, payment terms
- **Delivery Preferences**: Shipping method, delivery address, timing
- **Missing Information**: Areas that need clarification
- **Order Accuracy**: Overall assessment of the order details

## API Endpoints

- `GET /` - Main web interface
- `POST /submit` - Process order analysis
- `GET /docs` - API documentation (FastAPI auto-generated)

## Development

- **Add new packages**: `pip install package_name`
- **Update requirements**: `pip freeze > requirements.txt`
- **Deactivate venv**: `deactivate`
- **API documentation**: Visit http://localhost:8000/docs

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| Shopify Endpoint | Already configured in code | For Shopify integration |
| `USE_CUSTOM_GPT` | Use custom GPT assistant (true/false) | No |
| `CUSTOM_ASSISTANT_ID` | Your custom GPT assistant ID | If USE_CUSTOM_GPT=true |

## Troubleshooting

- **"OpenAI API key not configured"**: Make sure your `.env` file exists with the correct API key
- **"Transcription failed"**: Check that the audio file is valid and the transcription service is available
- **Port already in use**: Change the port in `main.py` or kill the existing process
- **Virtual environment activation issues**: Use `venv/Scripts/python main.py` directly on Windows

### Shopify Integration Issues

- **"Order not found"**: Verify the order ID exists in your Shopify system
- **"API error"**: Check that your Shopify endpoint is accessible and responding
- **"Request failed"**: Verify your endpoint URL is correct and the service is running

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and rotate them regularly
- The `.env` file is already in `.gitignore`

## Additional Documentation

- **Shopify Integration**: Uses your existing endpoint at `https://ziperp-api.vercel.app/api/shipment/`
