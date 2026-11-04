from flask import redirect, render_template, url_for, session, request, flash, Blueprint
from app import db
from .models.models import Product, User
from .utils import get_next_local_id, _t
from sqlalchemy import or_

products = Blueprint('products', __name__)

def format_currency(amount):

    return f"{amount:,}".replace(",", ".")

def create_sku(next_no):
    return f"PRD-{next_no:04d}"

def filter_by_condition(form):
    condition = form.get('product_status')

    if condition == 'low_stock':
        return Product.query.filter(Product.admin_id == session.get('workspace_id'), Product.stock < 10, Product.stock >= 1).all()
    elif condition:
        return Product.query.filter_by(admin_id = session.get('workspace_id'), status = condition).all()
    
    return db.session.get(User, session.get('workspace_id')).products

def has_low_stock(product):
    return 1 <= int(product.stock) < 10

def is_out_of_stock(product):
    return True if product.stock == 0 else False

@products.route("/products", methods=['POST', 'GET'])
def products_page():
    workspace_id = session.get('workspace_id')

    if not 'id' in session:
        return redirect(url_for('users.login'))

    products = db.session.get(User, session.get('workspace_id')).products

    if request.method == 'POST':    
        form = request.form
        products = filter_by_condition(form)
        action = request.form.get('action')
        keyword = form.get('search_products')

        if keyword:
            searched_products = Product.query.filter(
                Product.admin_id == session.get('workspace_id'),
                or_(
                    Product.name.like(f"%{keyword}%"),
                    Product.sku.like(f"%{keyword}%"),
                    Product.category.like(f"%{keyword}%"),
                    Product.status.like(f"%{keyword}%"),
                )
            ).all()  
        
            products = list(set(searched_products))

        if session.get('role') == 'admin':
            if action == 'add':
                prod_name = form.get('name')
                prod_price = float(form.get('price'))
                prod_stock = int(form.get('stock'))
                prod_category = form.get('category')

                request_status = form.get('status', 'active')
                prod_status = 'inactive' if prod_stock <= 0 else request_status
                prod_img_url = form.get('image_url')

                next_prod_no = get_next_local_id(Product, workspace_id)

                new_product = Product(
                    session.get('id'),
                    prod_name, 
                    prod_status,
                    prod_category,
                    prod_price,
                    prod_stock,
                    prod_img_url
                )

                new_product.local_id = next_prod_no
                new_product.sku = create_sku(next_prod_no)

                db.session.add(new_product)
                db.session.commit()

                flash(_t('toast_prod_created'), 'success')
                return redirect(url_for("products.products_page"))

            elif action == 'edit':
                prod_id = form.get('id')
                product = Product.query.filter_by(id=prod_id, admin_id=workspace_id).first()

                if product:
                    product.name = form.get('name', product.name)
                    product.category = form.get('category', product.category)
                    product.price = float(form.get('price', product.price))
                    
                    new_stock = int(form.get('stock', product.stock))
                    product.stock = new_stock

                    if new_stock <= 0:
                        product.status = 'inactive'
                    else:
                        product.status = form.get('status', 'active')

                    product.image_url = form.get('image_url', product.image_url)
                    db.session.commit()

                    flash(_t('toast_prod_updated'), 'success')
                    return redirect(url_for("products.products_page"))
                
            elif action == 'delete':
                prod_id = form.get('id')
                product = Product.query.filter_by(id=prod_id, admin_id=workspace_id).first()

                if prod_id and product:
                    Product.query.filter_by(id=prod_id, admin_id=workspace_id).delete()
                    db.session.commit()
                    flash(_t('toast_prod_deleted'), 'success')

                return redirect(url_for("products.products_page"))            

    return render_template('products.html', products = products, has_low_stock = has_low_stock, is_out_of_stock = is_out_of_stock, user = db.session.get(User, session.get('id')))
