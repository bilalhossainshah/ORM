/**
 * JWT Authentication Frontend Integration Example
 * This demonstrates how to implement JWT token handling in JavaScript
 * 
 * Use this as a template for your frontend application.
 */

// Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';
const TOKEN_KEY = 'access_token';

// ============================================================================
// 1. LOGIN - Get JWT Token
// ============================================================================

/**
 * Login user and store JWT token
 */
async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();

        // Store JWT token in localStorage
        localStorage.setItem(TOKEN_KEY, data.access_token);
        localStorage.setItem('user_id', data.user_id);
        localStorage.setItem('email', data.email);

        console.log('Login successful! Token stored.');
        return data;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

// ============================================================================
// 2. REGISTER - Create new user
// ============================================================================

/**
 * Register a new user
 */
async function register(email, password, fullName) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/register/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password,
                full_name: fullName,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }

        const data = await response.json();
        console.log('Registration successful!', data);
        return data;
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}

// ============================================================================
// 3. GET AUTH HEADER - Helper function for protected requests
// ============================================================================

/**
 * Get Authorization header with JWT token
 * Returns null if no token is stored (user not logged in)
 */
function getAuthHeader() {
    const token = localStorage.getItem(TOKEN_KEY);
    if (!token) {
        console.warn('No token found. User may not be logged in.');
        return null;
    }
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    };
}

// ============================================================================
// 4. PROTECTED REQUESTS - Add to cart, checkout, etc.
// ============================================================================

/**
 * Add item to cart (Protected - requires JWT)
 */
async function addToCart(productId, quantity) {
    try {
        const authHeader = getAuthHeader();
        if (!authHeader) {
            throw new Error('Not authenticated. Please login first.');
        }

        const userId = parseInt(localStorage.getItem('user_id'));

        const response = await fetch(`${API_BASE_URL}/cart/add-item/`, {
            method: 'POST',
            headers: authHeader,
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity,
                user_id: userId,
            }),
        });

        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Token expired. Please login again.');
            }
            const error = await response.json();
            throw new Error(error.detail || 'Failed to add item to cart');
        }

        const data = await response.json();
        console.log('Item added to cart:', data);
        return data;
    } catch (error) {
        console.error('Add to cart error:', error);
        throw error;
    }
}

/**
 * View cart/order details (Protected - requires JWT)
 */
async function viewCart(orderId) {
    try {
        const authHeader = getAuthHeader();
        if (!authHeader) {
            throw new Error('Not authenticated. Please login first.');
        }

        const response = await fetch(`${API_BASE_URL}/cart/${orderId}/`, {
            method: 'GET',
            headers: authHeader,
        });

        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Token expired. Please login again.');
            }
            const error = await response.json();
            throw new Error(error.detail || 'Failed to fetch cart');
        }

        const data = await response.json();
        console.log('Cart details:', data);
        return data;
    } catch (error) {
        console.error('View cart error:', error);
        throw error;
    }
}

/**
 * Process checkout (Protected - requires JWT)
 */
async function checkout(orderId) {
    try {
        const authHeader = getAuthHeader();
        if (!authHeader) {
            throw new Error('Not authenticated. Please login first.');
        }

        const response = await fetch(`${API_BASE_URL}/cart/${orderId}/checkout/`, {
            method: 'POST',
            headers: authHeader,
        });

        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Token expired. Please login again.');
            }
            const error = await response.json();
            throw new Error(error.detail || 'Checkout failed');
        }

        const data = await response.json();
        console.log('Checkout successful:', data);
        return data;
    } catch (error) {
        console.error('Checkout error:', error);
        throw error;
    }
}

// ============================================================================
// 5. LOGOUT - Clear stored token
// ============================================================================

/**
 * Logout user - clear stored token and user data
 */
function logout() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem('user_id');
    localStorage.removeItem('email');
    console.log('Logged out successfully');
}

/**
 * Check if user is logged in
 */
function isLoggedIn() {
    return localStorage.getItem(TOKEN_KEY) !== null;
}

/**
 * Get current user info
 */
function getCurrentUser() {
    return {
        user_id: localStorage.getItem('user_id'),
        email: localStorage.getItem('email'),
        token: localStorage.getItem(TOKEN_KEY),
    };
}

// ============================================================================
// 6. USAGE EXAMPLE - Integration in HTML
// ============================================================================

/*

HTML EXAMPLE:

<div id="auth-container">
    <div id="login-form" style="display: block;">
        <h2>Login</h2>
        <input type="email" id="login-email" placeholder="Email">
        <input type="password" id="login-password" placeholder="Password">
        <button onclick="handleLogin()">Login</button>
    </div>

    <div id="cart-section" style="display: none;">
        <h2>Shopping Cart</h2>
        <button onclick="handleLogout()">Logout</button>
        
        <div id="product-list"></div>
        
        <div>
            <input type="number" id="product-id" placeholder="Product ID">
            <input type="number" id="quantity" placeholder="Quantity" value="1">
            <button onclick="handleAddToCart()">Add to Cart</button>
        </div>

        <div>
            <input type="number" id="order-id" placeholder="Order ID">
            <button onclick="handleViewCart()">View Cart</button>
            <button onclick="handleCheckout()">Checkout</button>
        </div>
    </div>
</div>

JAVASCRIPT:

async function handleLogin() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        await login(email, password);
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('cart-section').style.display = 'block';
    } catch (error) {
        alert('Login failed: ' + error.message);
    }
}

function handleLogout() {
    logout();
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('cart-section').style.display = 'none';
}

async function handleAddToCart() {
    const productId = parseInt(document.getElementById('product-id').value);
    const quantity = parseInt(document.getElementById('quantity').value);
    
    try {
        await addToCart(productId, quantity);
        alert('Item added to cart!');
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function handleViewCart() {
    const orderId = parseInt(document.getElementById('order-id').value);
    
    try {
        await viewCart(orderId);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function handleCheckout() {
    const orderId = parseInt(document.getElementById('order-id').value);
    
    try {
        await checkout(orderId);
        alert('Checkout successful!');
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

*/

// Export functions for use in HTML or modules
export {
    login,
    register,
    addToCart,
    viewCart,
    checkout,
    logout,
    isLoggedIn,
    getCurrentUser,
    getAuthHeader,
};
