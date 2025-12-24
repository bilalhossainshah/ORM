"""
Test script to verify new cart endpoints are working correctly.
Tests update-item, remove-item, and enhanced checkout endpoints.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

# Test configuration
TEST_EMAIL = "testcart@example.com"
TEST_PASSWORD = "testpass123"
TEST_PRODUCT_ID = 1

def test_endpoints():
    print("=" * 60)
    print("TESTING CART ENDPOINTS")
    print("=" * 60)
    
    # Step 1: Register
    print("\n1. Registering user...")
    register_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "full_name": "Cart Test User"
    }
    resp = requests.post(f"{BASE_URL}/users/register/", json=register_data)
    if resp.status_code != 200:
        print(f"   ❌ Registration failed: {resp.text}")
        return False
    user = resp.json()
    user_id = user.get("id")
    print(f"   ✅ User registered: ID={user_id}")
    
    # Step 2: Login
    print("\n2. Logging in...")
    login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    resp = requests.post(f"{BASE_URL}/users/login/", json=login_data)
    if resp.status_code != 200:
        print(f"   ❌ Login failed: {resp.text}")
        return False
    token_response = resp.json()
    token = token_response.get("access_token")
    print(f"   ✅ Login successful, token obtained: {token[:20]}...")
    
    # Set up auth header
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: Create order/cart
    print("\n3. Creating order...")
    order_data = {"user_id": user_id, "status": "Pending"}
    resp = requests.post(
        f"{BASE_URL}/cart/create/",
        json=order_data,
        headers=headers
    )
    if resp.status_code not in [200, 201]:
        print(f"   ❌ Order creation failed: {resp.text}")
        # Try to use an existing order
        order_id = 1
        print(f"   Using order_id: {order_id}")
    else:
        order_id = resp.json().get("id")
        print(f"   ✅ Order created: ID={order_id}")
    
    # Step 4: Add item to cart
    print(f"\n4. Adding item to cart (order_id={order_id})...")
    add_item_data = {
        "user_id": user_id,
        "product_id": TEST_PRODUCT_ID,
        "quantity": 2
    }
    resp = requests.post(
        f"{BASE_URL}/cart/add-item/",
        json=add_item_data,
        headers=headers
    )
    if resp.status_code not in [200, 201]:
        print(f"   ❌ Add item failed: {resp.text}")
        return False
    cart_item = resp.json()
    item_id = cart_item.get("id")
    print(f"   ✅ Item added: ID={item_id}, quantity=2")
    
    # Step 5: Test UPDATE-ITEM endpoint
    print(f"\n5. Testing PUT /cart/update-item/{item_id}...")
    resp = requests.put(
        f"{BASE_URL}/cart/update-item/{item_id}?quantity=5",
        headers=headers
    )
    if resp.status_code != 200:
        print(f"   ❌ Update failed: {resp.text}")
        return False
    result = resp.json()
    print(f"   ✅ Item updated successfully")
    print(f"      Response: {json.dumps(result, indent=2)}")
    
    # Step 6: Test REMOVE-ITEM endpoint (add a second item first)
    print(f"\n6. Adding another item to test remove...")
    add_item_data["quantity"] = 1
    resp = requests.post(
        f"{BASE_URL}/cart/add-item/",
        json=add_item_data,
        headers=headers
    )
    if resp.status_code not in [200, 201]:
        print(f"   ❌ Second add failed: {resp.text}")
        return False
    cart_item2 = resp.json()
    item_id2 = cart_item2.get("id")
    print(f"   ✅ Second item added: ID={item_id2}")
    
    print(f"\n7. Testing DELETE /cart/remove-item/{item_id2}...")
    resp = requests.delete(
        f"{BASE_URL}/cart/remove-item/{item_id2}",
        headers=headers
    )
    if resp.status_code != 200:
        print(f"   ❌ Remove failed: {resp.text}")
        return False
    result = resp.json()
    print(f"   ✅ Item removed successfully")
    print(f"      Response: {json.dumps(result, indent=2)}")
    
    # Step 7: Test CHECKOUT endpoint with ShippingAddress
    print(f"\n8. Testing POST /cart/{order_id}/checkout/ with shipping...")
    checkout_data = {
        "order_id": order_id,
        "shipping_address": {
            "full_name": "Cart Test User",
            "email": TEST_EMAIL,
            "phone": "+1234567890",
            "street_address": "123 Test St",
            "city": "Test City",
            "state": "TC",
            "postal_code": "12345",
            "country": "Test Country"
        },
        "payment_method": "credit_card"
    }
    resp = requests.post(
        f"{BASE_URL}/cart/{order_id}/checkout/",
        json=checkout_data,
        headers=headers
    )
    if resp.status_code != 200:
        print(f"   ❌ Checkout failed: {resp.text}")
        return False
    confirmation = resp.json()
    print(f"   ✅ Checkout successful")
    print(f"      Response: {json.dumps(confirmation, indent=2)}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        success = test_endpoints()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        exit(1)
