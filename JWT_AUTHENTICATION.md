# JWT Authentication Implementation

## Overview

Your E-commerce API now includes complete JWT (JSON Web Token) authentication. Users must login to receive a token, which must be included in all protected API requests.

## Architecture

### Backend Components

1. **JWT Utilities** (`app/utils/jwt_utils.py`)
   - `create_access_token()` - Generates JWT tokens
   - `verify_token()` - Validates and decodes tokens
   - `TokenData` - Token payload schema
   - `TokenResponse` - Login response schema

2. **Dependencies** (`app/dependencies.py`)
   - `get_current_user()` - FastAPI dependency that verifies JWT tokens on protected routes

3. **User Router** (`app/routers/user.py`)
   - `POST /users/register/` - Register new user
   - `POST /users/login/` - Login and get JWT token
   - `GET /users/{user_id}` - Get user info

4. **Protected Routes** (`app/routers/cart.py`)
   - `POST /cart/add-item/` - Add item to cart (requires JWT)
   - `GET /cart/{order_id}/` - View cart (requires JWT)
   - `POST /cart/{order_id}/checkout/` - Checkout (requires JWT)

---

## Backend API Flow

### 1. Register User

**Endpoint:** `POST /users/register/`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "created_at": "2025-12-08T10:30:00"
}
```

### 2. Login & Get Token

**Endpoint:** `POST /users/login/`

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": 1,
  "email": "user@example.com"
}
```

**Token Details:**
- `access_token` - JWT token valid for 30 minutes (configurable)
- `token_type` - Always "bearer"
- `user_id` - User's database ID
- `email` - User's email address

### 3. Protected Route - Add to Cart

**Endpoint:** `POST /cart/add-item/`

**Headers (REQUIRED):**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request:**
```json
{
  "product_id": 1,
  "quantity": 2,
  "user_id": 1
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": 1,
  "product_id": 1,
  "quantity": 2,
  "price": 29.99
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - User ID in token doesn't match request

---

## Frontend Implementation

### 1. Installation

Copy `frontend_jwt_example.js` to your project and include it:

```html
<script src="path/to/frontend_jwt_example.js"></script>
```

Or import as module:
```javascript
import { login, register, addToCart, checkout, logout } from './frontend_jwt_example.js';
```

### 2. User Registration

```javascript
async function handleRegister() {
  try {
    const user = await register(
      'newuser@example.com',
      'password123',
      'John Doe'
    );
    console.log('Registered:', user);
  } catch (error) {
    console.error('Registration failed:', error);
  }
}
```

### 3. User Login

```javascript
async function handleLogin() {
  try {
    const response = await login('user@example.com', 'password123');
    console.log('Login successful!');
    console.log('Token:', response.access_token);
    console.log('User ID:', response.user_id);
    
    // Token is automatically stored in localStorage
    // Ready to make protected requests
  } catch (error) {
    console.error('Login failed:', error);
  }
}
```

### 4. Add Item to Cart (Protected)

```javascript
async function handleAddToCart() {
  try {
    const item = await addToCart(
      productId,  // Product ID
      quantity    // Quantity
    );
    console.log('Item added:', item);
  } catch (error) {
    if (error.message.includes('Token expired')) {
      // Redirect to login
      window.location.href = '/login';
    }
    console.error('Error:', error.message);
  }
}
```

### 5. View Cart (Protected)

```javascript
async function handleViewCart() {
  try {
    const cart = await viewCart(orderId);
    console.log('Cart contents:', cart);
    displayCartItems(cart.items);
  } catch (error) {
    console.error('Error viewing cart:', error);
  }
}
```

### 6. Checkout (Protected)

```javascript
async function handleCheckout() {
  try {
    const result = await checkout(orderId);
    console.log('Order status:', result.status);
    alert('Checkout successful!');
  } catch (error) {
    console.error('Checkout failed:', error);
    alert('Error: ' + error.message);
  }
}
```

### 7. Logout

```javascript
function handleLogout() {
  logout();
  // Redirect to login page
  window.location.href = '/login';
}
```

---

## Token Storage

Tokens are stored in browser's localStorage with key `access_token`:

```javascript
// Get token
const token = localStorage.getItem('access_token');

// Token is automatically included in all protected requests
// via getAuthHeader() function
```

**⚠️ Security Note:** In production, consider using:
- `sessionStorage` instead of `localStorage` (cleared on browser close)
- HTTP-only cookies with SameSite attribute
- Secure and HTTPS-only flags

---

## Complete HTML Example

```html
<!DOCTYPE html>
<html>
<head>
    <title>E-commerce with JWT</title>
    <script src="frontend_jwt_example.js"></script>
</head>
<body>
    <!-- Login Form -->
    <div id="login-section">
        <h2>Login</h2>
        <input type="email" id="email" placeholder="Email">
        <input type="password" id="password" placeholder="Password">
        <button onclick="handleLogin()">Login</button>
        <button onclick="toggleRegisterForm()">New User? Register</button>

        <div id="register-form" style="display:none; margin-top: 20px;">
            <h3>Register</h3>
            <input type="email" id="register-email" placeholder="Email">
            <input type="password" id="register-password" placeholder="Password">
            <input type="text" id="full-name" placeholder="Full Name">
            <button onclick="handleRegister()">Register</button>
        </div>
    </div>

    <!-- Shopping Cart Section -->
    <div id="shop-section" style="display:none;">
        <h2>Shopping</h2>
        <p>Welcome, <span id="user-email"></span>! <button onclick="handleLogout()">Logout</button></p>

        <!-- Add to Cart -->
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
            <h3>Add Item to Cart</h3>
            <input type="number" id="product-id" placeholder="Product ID">
            <input type="number" id="quantity" placeholder="Quantity" value="1">
            <button onclick="handleAddToCart()">Add to Cart</button>
            <div id="add-result"></div>
        </div>

        <!-- View Cart -->
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
            <h3>View Cart</h3>
            <input type="number" id="order-id" placeholder="Order ID">
            <button onclick="handleViewCart()">View Cart</button>
            <div id="cart-contents"></div>
        </div>

        <!-- Checkout -->
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
            <h3>Checkout</h3>
            <button onclick="handleCheckout()">Proceed to Checkout</button>
            <div id="checkout-result"></div>
        </div>
    </div>

    <script>
        // Helper functions
        async function handleLogin() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await login(email, password);
                document.getElementById('login-section').style.display = 'none';
                document.getElementById('shop-section').style.display = 'block';
                document.getElementById('user-email').textContent = response.email;
            } catch (error) {
                alert('Login failed: ' + error.message);
            }
        }

        async function handleRegister() {
            const email = document.getElementById('register-email').value;
            const password = document.getElementById('register-password').value;
            const fullName = document.getElementById('full-name').value;
            
            try {
                await register(email, password, fullName);
                alert('Registration successful! Please login.');
                document.getElementById('register-form').style.display = 'none';
                document.getElementById('register-email').value = '';
                document.getElementById('register-password').value = '';
                document.getElementById('full-name').value = '';
            } catch (error) {
                alert('Registration failed: ' + error.message);
            }
        }

        function toggleRegisterForm() {
            const form = document.getElementById('register-form');
            form.style.display = form.style.display === 'none' ? 'block' : 'none';
        }

        async function handleAddToCart() {
            const productId = parseInt(document.getElementById('product-id').value);
            const quantity = parseInt(document.getElementById('quantity').value);
            
            try {
                const result = await addToCart(productId, quantity);
                document.getElementById('add-result').textContent = 
                    `✓ Added item ${result.id} to cart!`;
            } catch (error) {
                document.getElementById('add-result').textContent = 
                    `✗ Error: ${error.message}`;
            }
        }

        async function handleViewCart() {
            const orderId = parseInt(document.getElementById('order-id').value);
            
            try {
                const cart = await viewCart(orderId);
                document.getElementById('cart-contents').innerHTML = 
                    `<pre>${JSON.stringify(cart, null, 2)}</pre>`;
            } catch (error) {
                document.getElementById('cart-contents').textContent = 
                    `✗ Error: ${error.message}`;
            }
        }

        async function handleCheckout() {
            const orderId = parseInt(document.getElementById('order-id').value);
            
            try {
                const result = await checkout(orderId);
                document.getElementById('checkout-result').textContent = 
                    `✓ Checkout successful! Status: ${result.status}`;
            } catch (error) {
                document.getElementById('checkout-result').textContent = 
                    `✗ Error: ${error.message}`;
            }
        }

        function handleLogout() {
            logout();
            document.getElementById('login-section').style.display = 'block';
            document.getElementById('shop-section').style.display = 'none';
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';
        }

        // Check if already logged in on page load
        window.addEventListener('load', () => {
            if (isLoggedIn()) {
                const user = getCurrentUser();
                document.getElementById('login-section').style.display = 'none';
                document.getElementById('shop-section').style.display = 'block';
                document.getElementById('user-email').textContent = user.email;
            }
        });
    </script>
</body>
</html>
```

---

## Configuration

### Token Expiration

Edit `app/utils/jwt_utils.py`:

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Change to desired minutes
```

### Secret Key (IMPORTANT!)

**CHANGE THIS IN PRODUCTION!**

In `app/utils/jwt_utils.py`:
```python
SECRET_KEY = "your-secret-key-change-this-in-production-12345"
```

Use environment variable:
```python
import os
SECRET_KEY = os.getenv("SECRET_KEY", "default-change-me")
```

---

## Testing with cURL

### 1. Register User
```bash
curl -X POST "http://127.0.0.1:8000/users/register/" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'
```

### 2. Login
```bash
curl -X POST "http://127.0.0.1:8000/users/login/" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### 3. Add to Cart (with token)
```bash
curl -X POST "http://127.0.0.1:8000/cart/add-item/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"quantity":2,"user_id":1}'
```

---

## Error Handling

### Common Errors

| Status | Error | Solution |
|--------|-------|----------|
| 401 | Invalid or expired token | Re-login to get new token |
| 403 | You can only add items to your own cart | Don't modify user_id in request |
| 400 | Email already registered | Use different email |
| 404 | User not found | Check user ID |

---

## Best Practices

1. **Always use HTTPS in production**
2. **Store sensitive data securely**
3. **Validate tokens on every protected request**
4. **Use short expiration times (15-30 minutes)**
5. **Implement refresh token mechanism** (optional)
6. **Never expose SECRET_KEY in frontend code**
7. **Use environment variables for configuration**

---

## Next Steps

- [x] Implement JWT authentication
- [ ] Add refresh token mechanism
- [ ] Implement role-based access control (admin/user)
- [ ] Add password reset functionality
- [ ] Implement email verification

