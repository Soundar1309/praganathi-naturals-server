# Ecommerce Django API Documentation

This document provides detailed information about the API endpoints, request/response formats, and authentication methods for the Django ecommerce application.

## Base URL
```
http://localhost:8000/api/
```

## Authentication

The API uses JWT (JSON Web Token) authentication. All protected endpoints require a valid JWT token in the Authorization header.

### Getting JWT Tokens

#### Register a new user
```http
POST /api/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "password": "securepassword123",
    "password_confirmation": "securepassword123",
    "role": "customer",
    "phone": "+1234567890"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "John",
        "last_name": "Doe",
        "role": "customer",
        "phone": "+1234567890",
        "date_joined": "2024-01-01T00:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### Login
```http
POST /api/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "securepassword123"
}
```

**Response:**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "John",
        "last_name": "Doe",
        "role": "customer",
        "phone": "+1234567890",
        "date_joined": "2024-01-01T00:00:00Z"
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### Using JWT Tokens
Include the access token in the Authorization header for all protected requests:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

#### Refresh Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Logout
```http
DELETE /api/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## User Management

### Get User Profile
```http
GET /api/profile/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer",
    "phone": "+1234567890",
    "date_joined": "2024-01-01T00:00:00Z"
}
```

### Update User Profile
```http
PUT /api/profile/update/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "Jane",
    "last_name": "Smith",
    "phone": "+1987654321"
}
```

## Address Management

### List User Addresses
```http
GET /api/addresses/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
    {
        "id": 1,
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "postal_code": "10001",
        "country": "US",
        "is_default": true,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

### Create Address
```http
POST /api/addresses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "street": "456 Oak Ave",
    "city": "Los Angeles",
    "state": "CA",
    "postal_code": "90210",
    "country": "US",
    "is_default": false
}
```

### Update Address
```http
PUT /api/addresses/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "street": "789 Pine St",
    "city": "Chicago",
    "state": "IL",
    "postal_code": "60601",
    "country": "US",
    "is_default": true
}
```

### Delete Address
```http
DELETE /api/addresses/1/
Authorization: Bearer <access_token>
```

## Products

### List Products
```http
GET /api/products/
```

**Query Parameters:**
- `category_id`: Filter by category ID
- `q`: Search in title and description
- `ordering`: Sort by field (e.g., `price`, `-created_at`)

**Example:**
```http
GET /api/products/?category_id=1&q=laptop&ordering=price
```

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "MacBook Pro",
            "description": "High-performance laptop",
            "price": "1299.99",
            "stock": 10,
            "image": "/media/products/macbook.jpg",
            "category": {
                "id": 1,
                "name": "Electronics",
                "description": "Electronic devices",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            "category_id": 1,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Get Product Details
```http
GET /api/products/1/
```

### Create Product (Admin Only)
```http
POST /api/products/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
    "title": "iPhone 15",
    "description": "Latest iPhone model",
    "price": "999.99",
    "stock": 50,
    "category_id": 1
}
```

### Update Product (Admin Only)
```http
PUT /api/products/1/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
    "title": "iPhone 15 Pro",
    "price": "1199.99",
    "stock": 25
}
```

### Delete Product (Admin Only)
```http
DELETE /api/products/1/
Authorization: Bearer <admin_token>
```

## Categories

### List Categories
```http
GET /api/categories/
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "Electronics",
        "description": "Electronic devices and gadgets",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

### Create Category
```http
POST /api/categories/
Content-Type: application/json

{
    "name": "Books",
    "description": "Books and literature"
}
```

## Shopping Cart

### Get User Cart
```http
GET /api/carts/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "id": 1,
    "cart_items": [
        {
            "id": 1,
            "product": {
                "id": 1,
                "title": "MacBook Pro",
                "description": "High-performance laptop",
                "price": "1299.99",
                "stock": 10,
                "image": "/media/products/macbook.jpg",
                "category": {
                    "id": 1,
                    "name": "Electronics",
                    "description": "Electronic devices",
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                },
                "category_id": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            },
            "product_id": 1,
            "quantity": 2,
            "subtotal": "2599.98",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ],
    "total": "2599.98",
    "item_count": 1,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Add Item to Cart
```http
POST /api/cart_items/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "product_id": 1,
    "quantity": 1
}
```

### Update Cart Item
```http
PUT /api/cart_items/1/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "quantity": 3
}
```

### Remove Item from Cart
```http
DELETE /api/cart_items/1/
Authorization: Bearer <access_token>
```

## Orders

### List Orders
```http
GET /api/orders/
Authorization: Bearer <access_token>
```

**Response (Customer):**
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "email": "user@example.com",
            "username": "username",
            "first_name": "John",
            "last_name": "Doe",
            "role": "customer",
            "phone": "+1234567890",
            "date_joined": "2024-01-01T00:00:00Z"
        },
        "address": {
            "id": 1,
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "US",
            "is_default": true,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        },
        "delivery": null,
        "status": "pending",
        "total": "2599.98",
        "order_items": [
            {
                "id": 1,
                "product": {
                    "id": 1,
                    "title": "MacBook Pro",
                    "description": "High-performance laptop",
                    "price": "1299.99",
                    "stock": 8,
                    "image": "/media/products/macbook.jpg",
                    "category": {
                        "id": 1,
                        "name": "Electronics",
                        "description": "Electronic devices",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z"
                    },
                    "category_id": 1,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                },
                "quantity": 2,
                "price": "1299.99",
                "subtotal": "2599.98",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ],
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

### Create Order
```http
POST /api/orders/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "address_id": 1
}
```

### Update Order Status (Admin/Delivery)
```http
PATCH /api/orders/1/
Authorization: Bearer <admin_token>
Content-Type: application/json

{
    "status": "shipped",
    "delivery_id": 2
}
```

## Notifications

### List Notifications
```http
GET /api/notifications/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
    {
        "id": 1,
        "message": "Your order status changed to shipped",
        "read": false,
        "notifiable": {
            "id": 1,
            "status": "shipped"
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
]
```

### Mark Notification as Read
```http
PATCH /api/notifications/1/read/
Authorization: Bearer <access_token>
```

### Mark All Notifications as Read
```http
PATCH /api/notifications/mark_all_read/
Authorization: Bearer <access_token>
```

### Delete All Notifications
```http
DELETE /api/notifications/destroy_all/
Authorization: Bearer <access_token>
```

### Get Unread Count
```http
GET /api/notifications/unread_count/
Authorization: Bearer <access_token>
```

**Response:**
```json
{
    "unread_count": 5
}
```

## Error Responses

### Validation Error
```json
{
    "errors": {
        "email": ["This field is required."],
        "password": ["This password is too short."]
    }
}
```

### Authentication Error
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Permission Error
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### Not Found Error
```json
{
    "detail": "Not found."
}
```

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content returned
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

The API implements rate limiting to prevent abuse. Limits are:
- 1000 requests per hour for authenticated users
- 100 requests per hour for anonymous users

## Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

**Response format:**
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/products/?page=2",
    "previous": null,
    "results": [...]
}
```

## File Upload

For file uploads (e.g., product images), use `multipart/form-data`:

```http
POST /api/products/
Authorization: Bearer <admin_token>
Content-Type: multipart/form-data

{
    "title": "Product with Image",
    "description": "Product description",
    "price": "99.99",
    "stock": 10,
    "category_id": 1,
    "image": <file>
}
```

## WebSocket Support

For real-time notifications, the application supports WebSocket connections:

```javascript
const socket = new WebSocket('ws://localhost:8000/ws/notifications/');

socket.onmessage = function(event) {
    const notification = JSON.parse(event.data);
    console.log('New notification:', notification);
};
``` 