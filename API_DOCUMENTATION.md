# Django E-commerce API Documentation

This document provides a detailed overview of the API endpoints and pages for the Django E-commerce project.

## Project Structure

The project is divided into three main Django apps:

-   `core`: Handles the core e-commerce functionalities like products, categories, vendors, cart, and wishlist.
-   `userauths`: Manages user authentication, registration, and user profiles.
-   `blog`: Provides blogging functionality.

---

## Core App

The `core` app is the heart of the e-commerce platform.

| URL Endpoint | View Function | Description |
|---|---|---|
| `/` | `index` | Displays the homepage of the website. |
| `/products/` | `products_list_view` | Lists all available products with optional filtering. |
| `/product/<pid>/` | `product_detail_view` | Shows the detailed view of a single product. |
| `/categories/` | `category_list_view` | Displays a list of all product categories. |
| `/category/<cid>/` | `category_product_list_view` | Lists all products belonging to a specific category. |
| `/vendors/` | `vendor_list_view` | Shows a list of all vendors. |
| `/vendor/<vid>/` | `vendor_detail_view` | Displays the profile and products of a specific vendor. |
| `/tags/<slug>/` | `tags_list` | Lists products associated with a specific tag. |
| `/ajax/add-review/<pid>/` | `ajax_add_review` | Handles the AJAX request to add a product review. |
| `/search/` | `search_view` | Provides search functionality for products. |
| `/filter-products/` | `filter_product` | Handles AJAX requests to filter products based on various criteria. |
| `/add-to-cart/` | `add_to_cart` | Handles the logic for adding a product to the shopping cart. |
| `/cart/` | `cart_view` | Displays the user's shopping cart. |
| `/delete-from-cart/` | `delete_from_cart` | Deletes an item from the shopping cart. |
| `/update-cart/` | `update_cart` | Updates the quantity of an item in the shopping cart. |
| `/wishlist/` | `wishlist_view` | Displays the user's wishlist. |
| `/add-to-wishlist/` | `add_to_wishlist` | Adds a product to the user's wishlist. |
| `/remove-from-wishlist/` | `remove_from_wishlist` | Removes a product from the user's wishlist. |
| `/contact/` | `contact` | Displays the contact page. |
| `/ajax-contact-form/` | `ajax_contact_form` | Handles the AJAX submission of the contact form. |
| `/about/` | `about` | Displays the about us page. |

---

## Userauths App

The `userauths` app handles user authentication and profile management.

| URL Endpoint | View Function | Description |
|---|---|---|
| `/user/sign-up/` | `register_view` | Renders the registration page and handles user sign-up. |
| `/user/sign-in/` | `login_view` | Renders the login page and handles user sign-in. |
| `/user/sign-out/` | `logout_view` | Logs the user out. |
| `/user/account/` | `account` | Displays the user's account page. |

---

## Blog App

The `blog` app provides blogging functionality.

| URL Endpoint | View Function | Description |
|---|---|---|
| `/blog/` | `blog_view` | Displays the main blog page with a list of posts. |
| `/blog/<pid>/` | `blog_detail_view` | Shows the detailed view of a single blog post. |
| `/blog/category/<cid>/` | `blog_category_view` | Lists all blog posts within a specific category. |
| `/blog/tags/<slug>/` | `blog_tags` | Lists all blog posts with a specific tag. |
| `/ajax-add-comment/<pid>/` | `ajax_add_comment` | Handles the AJAX request to add a comment to a blog post. |