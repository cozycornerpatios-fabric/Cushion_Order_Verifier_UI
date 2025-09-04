# Shopify Integration Setup Guide

This guide will help you set up Shopify integration to automatically pull order details into the Cushion Order Verifier UI.

## Prerequisites

- Your Shopify order details endpoint is already configured at `https://ziperp-api.vercel.app/api/shipment/`
- You have valid Shopify order numbers to test with
- Basic understanding of API integrations

## Step 1: Verify Your Endpoint

Your Shopify order details endpoint is already configured and ready to use:
- **Endpoint URL**: `https://ziperp-api.vercel.app/api/shipment/{orderNumber}`
- **Method**: GET
- **Response**: JSON with order details or error message

## Step 2: Test the Integration

1. **Find a Valid Order Number**
   - Use a real Shopify order number from your system
   - The endpoint expects numeric order numbers only

2. **Test the Endpoint**
   ```bash
   curl "https://ziperp-api.vercel.app/api/shipment/YOUR_ORDER_NUMBER"
   ```

3. **Expected Responses**
   - **Success**: JSON with order details
   - **Not Found**: `{"error":"Product properties not found, check for the right order number."}`
   - **Invalid Input**: `{"error":"Failed to get product properties","details":"invalid input syntax for type bigint: \"test\""}`

## Step 3: Test the Application

1. **Start Your Application**
   ```bash
   python main.py
   ```

2. **Test with a Real Order Number**
   - Use a valid Shopify order number from your system
   - In the app, select "Shopify" as order source
   - Enter the order number (numeric only)
   - Click "Verify Order"

## Finding Order Numbers

### Method 1: From Shopify Admin
1. Go to **Orders** in your Shopify admin
2. Click on any order
3. Look for the **Order Number** (usually displayed prominently)
4. This is the numeric value you need for the API

### Method 2: From Order Details
1. Open any order in your admin
2. Look for **Order Number** in the order information
3. This is the numeric ID you need for the endpoint

### Method 3: From Order Export
1. Go to **Orders** → **Export**
2. Export orders as CSV
3. Look for the **Order Number** column

## Troubleshooting

### Common Issues

1. **"Order not found"**
   - Verify the order number exists in your Shopify system
   - Make sure you're using the correct numeric order number
   - Check that the order is not archived or deleted

2. **"Invalid input syntax for type bigint"**
   - Ensure you're entering only numeric values
   - Remove any letters, spaces, or special characters
   - The endpoint only accepts numeric order numbers

3. **"Product properties not found"**
   - The order number exists but has no product details
   - Try with a different order number
   - Check if the order has been processed correctly in Shopify

4. **"Request failed" or "Connection error"**
   - Check your internet connection
   - Verify the endpoint URL is accessible
   - Try again after a few moments

### API Rate Limits

- Your endpoint may have rate limits
- If you encounter rate limiting, wait a moment and try again
- Contact your API provider if you need higher rate limits

## Security Best Practices

1. **Keep API Endpoints Secure**
   - Never expose sensitive order data in logs
   - Use HTTPS for all API communications
   - Monitor API usage and access patterns

2. **Data Privacy**
   - Only access order data you need for verification
   - Don't store sensitive customer information unnecessarily
   - Follow data protection regulations

3. **Monitor API Usage**
   - Check API response times and error rates
   - Monitor for unusual access patterns
   - Contact your API provider if you notice issues

## Support

If you encounter issues:

1. Check the application logs for detailed error messages
2. Verify your order number is correct and numeric
3. Test the endpoint directly with curl first
4. Ensure your API endpoint is accessible and responding

## Next Steps

Once Shopify integration is working:

1. **Test with Various Order Types**
   - Simple orders
   - Orders with custom properties
   - Orders with multiple line items

2. **Optimize Your Workflow**
   - Use Shopify integration for Shopify orders
   - Use manual input for other sources (Zendesk, Etsy, etc.)

3. **Monitor Performance**
   - Check API response times
   - Monitor error rates
   - Optimize based on usage patterns
