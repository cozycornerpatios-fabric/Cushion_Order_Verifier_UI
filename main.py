from fastapi import FastAPI, Form, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import logging
import json
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API endpoints
GPT_ENDPOINT = "https://api.openai.com/v1/chat/completions"
ASSISTANTS_ENDPOINT = "https://api.openai.com/v1/assistants"
THREADS_ENDPOINT = "https://api.openai.com/v1/threads"
MESSAGES_ENDPOINT = "https://api.openai.com/v1/threads/{thread_id}/messages"
RUNS_ENDPOINT = "https://api.openai.com/v1/threads/{thread_id}/runs"
WHISPER_ENDPOINT = "https://api.openai.com/v1/audio/transcriptions"  # OpenAI Whisper API


SHOPIFY_ORDER_ENDPOINT = "https://ziperp-api.vercel.app/api/shopify/"

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CUSTOM_ASSISTANT_ID = os.getenv("CUSTOM_ASSISTANT_ID")  # Your custom GPT assistant ID
USE_CUSTOM_GPT = os.getenv("USE_CUSTOM_GPT", "false").lower() == "true"

logger.info("Application started")
logger.info(f"OpenAI API Key configured: {'Yes' if OPENAI_API_KEY else 'No'}")
logger.info(f"Custom Assistant ID configured: {'Yes' if CUSTOM_ASSISTANT_ID else 'No'}")
logger.info(f"Use Custom GPT: {USE_CUSTOM_GPT}")
logger.info(f"Shopify Order Endpoint: {SHOPIFY_ORDER_ENDPOINT}")

def fetch_shopify_order(order_id: str) -> str:
    """
    Fetch order details from your Shopify endpoint
    """
    try:
        # Construct the full URL with order ID
        encoded_order_id = quote(order_id, safe='')
        url = f"{SHOPIFY_ORDER_ENDPOINT}{encoded_order_id}"
        
        
        logger.info(f"Fetching Shopify order from: {url}")
        
        # Make the request to your endpoint
        response = requests.get(url, timeout=30)
        
        if response.status_code == 404:
            raise Exception(f"Order {order_id} not found")
        elif not response.ok:
            raise Exception(f"API error: {response.status_code} - {response.text}")
        
        # Parse the response
        order_data = response.json()
        
        # Format the order details for verification
        # Adjust this based on your actual API response structure
        formatted_order = f"""Shopify Order Details:
Order ID: {order_id}
Order Data: {json.dumps(order_data, indent=2)}"""
        
        logger.info(f"Successfully fetched Shopify order {order_id}")
        return formatted_order
        
    except requests.exceptions.Timeout:
        logger.error(f"Request timed out for order {order_id}")
        raise Exception("Request timed out. Please try again.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for order {order_id}: {str(e)}")
        raise Exception(f"Failed to connect to Shopify endpoint: {str(e)}")
    except Exception as e:
        logger.error(f"Error fetching Shopify order {order_id}: {str(e)}")
        raise

def call_custom_gpt_assistant(final_order, customer_context=""):
    """
    Call a custom GPT assistant using OpenAI's Assistants API
    """
    if not CUSTOM_ASSISTANT_ID:
        raise ValueError("Custom Assistant ID not configured")
    
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API Key not configured")
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
        "OpenAI-Beta": "assistants=v2"
    }
    
    try:
        logger.info(f"Creating thread with assistant ID: {CUSTOM_ASSISTANT_ID}")
        
        # Create a new empty thread
        thread_response = requests.post(THREADS_ENDPOINT, headers=headers, json={})
        
        # Log the response for debugging
        logger.info(f"Thread creation response status: {thread_response.status_code}")
        logger.info(f"Thread creation response: {thread_response.text}")
        
        if not thread_response.ok:
            logger.error(f"Thread creation failed: {thread_response.status_code} - {thread_response.text}")
            raise Exception(f"Thread creation failed: {thread_response.status_code} - {thread_response.text}")
        
        thread_id = thread_response.json()["id"]
        logger.info(f"Thread created successfully with ID: {thread_id}")
        
        # Prepare the complete message with final order and customer context
        complete_message = f"""Please analyze the following order for verification and provide results in this EXACT format:

VERIFICATION RESULTS:
Cushion Type: Missing/Unclear (Type of cushion such as seat, back, etc. not explicitly mentioned)
Shape: Mismatch (Order mentions rectangular; Audio specifies trapezoidal)
Dimensions: Mismatch (Order: 30" x 41"; Audio: Width unclear, Length unclear, Height 12", Depth 3")
Fabric: Mismatch (Order: Chenille-Pearl; Audio: Agora 61 or Sunbrella SJ)
Color or Pattern: Mismatch (Order: Pearl; Audio: Specific pattern/color not mentioned)
Foam or Fill Type: Mismatch (Order: Fiber Fill; Audio suggests typical cushion cover fill)
Ties: Match (No ties requested)
Piping: Mismatch (Order: Piping; Audio: No piping requested)
Quantity per type/variant: Match (Quantity: 1)
Special Requests: Missing/Unclear (No specific customer instructions are provided in the audio)

CRITICAL REQUIREMENTS:
- Start with "VERIFICATION RESULTS:" on its own line
- Use exactly this format: "Attribute: Status (Details)" for each line
- Status must be exactly one of: Match, Mismatch, Missing/Unclear
- Include details in parentheses for every attribute
- Do not add any extra text, explanations, or formatting before or after the verification results
- Focus on cushion-specific attributes like type, shape, dimensions, fabric, color, foam, ties, piping, quantity, and special requests

Final Order for Verification:
{final_order}"""

        if customer_context:
            complete_message += f"""

Customer Communication Context:
{customer_context}"""
        
        # Add the user message to the thread
        message_data = {
            "role": "user",
            "content": complete_message
        }
        
        logger.info(f"Adding message to thread: {complete_message[:100]}...")
        message_response = requests.post(
            MESSAGES_ENDPOINT.format(thread_id=thread_id),
            headers=headers,
            json=message_data
        )
        
        if not message_response.ok:
            logger.error(f"Message creation failed: {message_response.status_code} - {message_response.text}")
            raise Exception(f"Message creation failed: {message_response.status_code} - {message_response.text}")
        
        logger.info("Message added successfully")
        
        # Create a run with the custom assistant
        run_data = {"assistant_id": CUSTOM_ASSISTANT_ID}
        logger.info(f"Creating run with assistant ID: {CUSTOM_ASSISTANT_ID}")
        
        run_response = requests.post(
            RUNS_ENDPOINT.format(thread_id=thread_id), 
            headers=headers, 
            json=run_data
        )
        
        if not run_response.ok:
            logger.error(f"Run creation failed: {run_response.status_code} - {run_response.text}")
            raise Exception(f"Run creation failed: {run_response.status_code} - {run_response.text}")
        
        run_id = run_response.json()["id"]
        logger.info(f"Run created successfully with ID: {run_id}")
        
        # Poll for completion
        max_attempts = 30
        for attempt in range(max_attempts):
            run_status_response = requests.get(
                RUNS_ENDPOINT.format(thread_id=thread_id) + f"/{run_id}",
                headers=headers
            )
            
            if not run_status_response.ok:
                logger.error(f"Run status check failed: {run_status_response.status_code} - {run_status_response.text}")
                raise Exception(f"Run status check failed: {run_status_response.status_code} - {run_status_response.text}")
            
            status = run_status_response.json()["status"]
            logger.info(f"Run status (attempt {attempt + 1}/{max_attempts}): {status}")
            
            if status == "completed":
                break
            elif status in ["failed", "cancelled", "expired"]:
                logger.error(f"Run {status}: {run_status_response.json()}")
                raise Exception(f"Run {status}: {run_status_response.json()}")
            
            import time
            time.sleep(2)  # Wait 2 seconds before checking again
        
        if status != "completed":
            raise Exception(f"Run did not complete within {max_attempts * 2} seconds")
        
        # Get the messages from the thread
        messages_response = requests.get(
            MESSAGES_ENDPOINT.format(thread_id=thread_id),
            headers=headers
        )
        
        if not messages_response.ok:
            logger.error(f"Messages retrieval failed: {messages_response.status_code} - {messages_response.text}")
            raise Exception(f"Messages retrieval failed: {messages_response.status_code} - {messages_response.text}")
        
        messages = messages_response.json()["data"]
        
        # Find the assistant's response (the last message from assistant)
        assistant_messages = [msg for msg in messages if msg["role"] == "assistant"]
        if not assistant_messages:
            raise Exception("No assistant response found")
        
        # Get the content from the last assistant message
        last_assistant_message = assistant_messages[-1]
        content = last_assistant_message["content"]
        
        # Extract text from content (content is a list of content blocks)
        if isinstance(content, list) and len(content) > 0:
            text_content = content[0].get("text", {}).get("value", "")
        else:
            text_content = str(content)
        
        logger.info(f"Custom GPT response received, length: {len(text_content)}")
        return text_content
        
    except Exception as e:
        logger.error(f"Error calling custom GPT assistant: {str(e)}")
        raise

def call_standard_gpt(final_order, customer_context=""):
    """
    Call standard GPT-4 using chat completions API
    """
    # Prepare the complete message with final order and customer context
    complete_message = f"Final Order for Verification:\n{final_order}"
    
    if customer_context:
        complete_message += f"\n\nCustomer Communication Context:\n{customer_context}"
    
    messages = [
        {"role": "system", "content": """You are an expert cushion order verifier. Your task is to:

1. Analyze the final order that needs verification
2. Use any provided customer communication context to understand the original requirements
3. Provide a comprehensive verification analysis in the following EXACT format:

VERIFICATION RESULTS:
Cushion Type: Missing/Unclear (Type of cushion such as seat, back, etc. not explicitly mentioned)
Shape: Mismatch (Order mentions rectangular; Audio specifies trapezoidal)
Dimensions: Mismatch (Order: 30" x 41"; Audio: Width unclear, Length unclear, Height 12", Depth 3")
Fabric: Mismatch (Order: Chenille-Pearl; Audio: Agora 61 or Sunbrella SJ)
Color or Pattern: Mismatch (Order: Pearl; Audio: Specific pattern/color not mentioned)
Foam or Fill Type: Mismatch (Order: Fiber Fill; Audio suggests typical cushion cover fill)
Ties: Match (No ties requested)
Piping: Mismatch (Order: Piping; Audio: No piping requested)
Quantity per type/variant: Match (Quantity: 1)
Special Requests: Missing/Unclear (No specific customer instructions are provided in the audio)

CRITICAL REQUIREMENTS:
- Start with "VERIFICATION RESULTS:" on its own line
- Use exactly this format: "Attribute: Status (Details)" for each line
- Status must be exactly one of: Match, Mismatch, Missing/Unclear
- Include details in parentheses for every attribute
- Do not add any extra text, explanations, or formatting before or after the verification results
- Focus on cushion-specific attributes like type, shape, dimensions, fabric, color, foam, ties, piping, quantity, and special requests"""},
        {"role": "user", "content": complete_message}
    ]

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4",
        "messages": messages,
        "temperature": 0
    }

    response = requests.post(GPT_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]

async def process_audio_file(audio_file, file_type):
    """
    Process audio file and return transcript using OpenAI Whisper API
    """
    if not audio_file or audio_file.size == 0:
        return ""
    
    logger.info(f"Processing {file_type} audio file: {audio_file.filename}, size: {audio_file.size}")
    
    # Read the audio file ONCE and store the bytes
    try:
        audio_bytes = await audio_file.read()
        file_size_mb = len(audio_bytes) / (1024 * 1024)
        logger.info(f"Audio file read successfully, size: {len(audio_bytes)} bytes ({file_size_mb:.1f} MB)")
        
        # Check file size limits for Whisper API
        if file_size_mb > 25:
            raise Exception(f"Audio file too large ({file_size_mb:.1f} MB). Whisper API supports files up to 25 MB.")
            
    except Exception as e:
        logger.error(f"Error reading {file_type} audio file: {str(e)}")
        raise Exception(f"Error reading {file_type} audio file: {str(e)}")
    
    # Use OpenAI Whisper API for transcription
    try:
        logger.info(f"Transcribing {file_type} audio with OpenAI Whisper API")
        
        # Prepare the file for Whisper API
        files = {"file": (audio_file.filename, audio_bytes, audio_file.content_type)}
        data = {"model": "whisper-1"}  # Use the latest Whisper model
        
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Whisper API has much longer timeout limits and handles large files better
        response = requests.post(WHISPER_ENDPOINT, headers=headers, files=files, data=data, timeout=600)  # 10 minutes
        
        if response.ok:
            transcript = response.json().get("text", "")
            logger.info(f"{file_type} Whisper transcription successful, length: {len(transcript)}")
            return transcript
        else:
            logger.error(f"{file_type} Whisper transcription failed: {response.status_code} - {response.text}")
            raise Exception(f"{file_type} Whisper transcription failed: {response.status_code} - {response.text}")
            
    except requests.exceptions.Timeout:
        logger.error(f"{file_type} Whisper transcription timed out after 10 minutes")
        raise Exception(f"{file_type} Whisper transcription timed out. The audio file may be too large or complex. Please try with a shorter audio file.")
    except Exception as e:
        logger.error(f"Error with {file_type} Whisper transcription: {str(e)}")
        raise

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    logger.info(f"GET / - Serving main page")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/shopify/orders/{order_id}")
async def get_shopify_order(order_id: str):
    """
    Get Shopify order data from your endpoint
    """
    try:
        order_data = fetch_shopify_order(order_id)
        return JSONResponse(content={"order": order_data})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/submit", response_class=HTMLResponse)
async def handle_form(
    request: Request,
    order_source: str = Form(...),  # Required field - "shopify" or "manual"
    final_order: str = Form(""),  # Optional when using Shopify
    shopify_order_id: str = Form(""),  # Optional when using manual input
    customer_chat_text: str = Form(""),
    customer_audio_file: UploadFile = File(None)
):
    logger.info("POST /submit - Form submission received")
    logger.info(f"Order source: {order_source}")
    logger.info(f"Final order provided: {'Yes' if final_order else 'No'}")
    logger.info(f"Shopify order ID provided: {'Yes' if shopify_order_id else 'No'}")
    logger.info(f"Customer chat text provided: {'Yes' if customer_chat_text else 'No'}")
    logger.info(f"Customer audio file provided: {'Yes' if customer_audio_file else 'No'}")
    
    # Validate order source and get final order details
    final_order_details = ""
    if order_source == "shopify":
        if not shopify_order_id or not shopify_order_id.strip():
            logger.warning("No Shopify order ID provided")
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": "Shopify order ID is required when selecting Shopify as order source."
            })
        
        try:
            final_order_details = fetch_shopify_order(shopify_order_id)
            logger.info(f"Successfully fetched Shopify order details, length: {len(final_order_details)}")
        except Exception as e:
            logger.error(f"Error fetching Shopify order: {str(e)}")
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": f"Error fetching Shopify order: {str(e)}"
            })
    else:  # manual input
        if not final_order or not final_order.strip():
            logger.warning("No final order provided")
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": "Final order for verification is required when using manual input."
            })
        final_order_details = final_order
    
    # Check if at least one customer communication method is provided
    if not customer_chat_text.strip() and not customer_audio_file:
        logger.warning("No customer communication provided")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "You must provide either customer communication text or audio file (or both)."
        })
    
    # Process customer audio if provided
    customer_transcript = ""
    if customer_audio_file:
        try:
            customer_transcript = await process_audio_file(customer_audio_file, "customer")
        except Exception as e:
            return templates.TemplateResponse("index.html", {
                "request": request,
                "error": f"Error processing customer audio file: {str(e)}"
            })
    
    # Combine customer context
    customer_context = ""
    if customer_chat_text and customer_transcript:
        customer_context = f"Chat Text: {customer_chat_text}\n\nAudio Transcript: {customer_transcript}"
    elif customer_chat_text:
        customer_context = customer_chat_text
    elif customer_transcript:
        customer_context = customer_transcript
    
    logger.info(f"Final order details length: {len(final_order_details)}")
    logger.info(f"Customer context length: {len(customer_context)}")
    
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key not configured")
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "OpenAI API key not configured."
        })

    try:
        if USE_CUSTOM_GPT:
            logger.info("Calling custom GPT assistant...")
            gpt_text = call_custom_gpt_assistant(final_order_details, customer_context)
            logger.info(f"Custom GPT assistant response successful, length: {len(gpt_text)}")
        else:
            logger.info("Calling standard GPT-4...")
            gpt_text = call_standard_gpt(final_order_details, customer_context)
            logger.info(f"Standard GPT-4 response successful, length: {len(gpt_text)}")
    except Exception as e:
        logger.error(f"Error calling GPT API: {str(e)}", exc_info=True)
        gpt_text = f"Error calling GPT API: {str(e)}"

    logger.info("Rendering response template...")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": gpt_text,
        "order_source": order_source,
        "final_order": final_order_details,
        "shopify_order_id": shopify_order_id,
        "customer_chat_text": customer_chat_text,
        "customer_transcript": customer_transcript
    })

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}", exc_info=True)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "error": f"An unexpected error occurred: {str(exc)}"
    })



if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
