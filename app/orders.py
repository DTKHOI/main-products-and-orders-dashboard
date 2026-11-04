from flask import redirect, render_template, url_for, session, request, flash, Blueprint, abort
from app import db
from .models.models import Product, Order, OrderItem, User
import json
from .utils import get_next_local_id, _t

orders = Blueprint('orders', __name__)

def read_cart_data(cart_data):
    if cart_data:
        try:
            cart_items = json.loads(cart_data)
        except json.JSONDecodeError:
            cart_items = []
    else: cart_items = []

    return cart_items

def create_ord(next_order_no):
    return f"ORD-{next_order_no:06d}"

def create_customer_id(next_order_no):
    return f"CUS-{next_order_no:06d}"

def total(products):
    total = 0
    workspace_id = session.get('workspace_id')

    for item in products:
        stored_item = Product.query.filter_by(id = item.get('id'), admin_id = workspace_id).first()
        buy_qty = item.get('quantity')

        if not stored_item or stored_item.stock < buy_qty:
            item_name = stored_item.name if stored_item else ""
            flash(f"{item_name} {_t('toast_stock_exceeded')}", 'error')
            return redirect(url_for('orders.orders_page'))
        
        total += buy_qty * float(item.get('price')) 

    return total

def create_order(cart_items, form):
    workspace_id = session.get('workspace_id')

    customer_name = form.get('customer_name')
    phone = form.get('phone')
    address = form.get('address')

    next_order_no = get_next_local_id(Order, workspace_id)

    new_order = Order(workspace_id, customer_name, shipping_address = address, total_amount = total(cart_items), customer_phone=phone)

    new_order.local_id = next_order_no
    new_order.customer_id = create_customer_id(next_order_no)
    new_order.ord = create_ord(next_order_no)

    db.session.add(new_order)
    db.session.commit()

    return new_order

def create_order_items(items, order_id):
    for item in items: 
        item_id = item.get('id')
        name = item.get('name')
        price = item.get('price')
        quantity = item.get('quantity')

        workspace_id = session.get('workspace_id')

        product = Product.query.filter_by(id = item_id, admin_id = workspace_id).first()
        if not product:
            flash(_t('toast_prod_not_found'), 'error')
            return

        new_order_item = OrderItem(order_id, name, quantity, price, product.sku, item_id)

        db.session.add(new_order_item)
    db.session.commit()

def reduce_stock(products):
    workspace_id = session.get('workspace_id')

    for prod in products:
        product = Product.query.filter_by(id = prod.get('id'), admin_id = workspace_id).first()
        product.stock -= prod.get('quantity')
    db.session.commit()

def restock_returned_item(items):
    workspace_id = session.get('workspace_id')

    for item in items:
        product_id = item.product_id
        returned_item = Product.query.filter_by(id = product_id, admin_id = workspace_id).first()

        if returned_item:
            returned_item.stock += item.quantity
    db.session.commit()

def filter_by_condition(form):
    condition = form.get('order_status')
    if condition:
        return Order.query.filter_by(admin_id = session.get('workspace_id'), status = condition).all()
    
    return db.session.get(User, session.get('workspace_id')).orders

@orders.route("/orders", methods=['GET', 'POST'])
def orders_page():
    if not 'id' in session:
        return redirect(url_for('users.login'))

    workspace_id = session.get('workspace_id')
    orders = Order.query.filter_by(admin_id = session.get('workspace_id')).all()

    if request.method == 'POST':
        form = request.form
        action = form.get('action')
        keyword = form.get('search_orders')
        orders = filter_by_condition(form)
        
        if keyword:
            from sqlalchemy import or_
            searched_orders = db.session.query(Order).filter(
                Order.admin_id == session.get('workspace_id'), 
                or_(
                    Order.ord.like(f"%{keyword}%"),
                    Order.customer_name.like(f"%{keyword}%"),
                    Order.customer_id.like(f"%{keyword}%"),
                    Order.customer_phone.like(f"%{keyword}%"),
                    Order.shipping_address.like(f"%{keyword}%"),
                    Order.total_amount.like(f"%{keyword}%"),
                    Order.created_at.like(f"%{keyword}%"),
                    Order.status.like(f"%{keyword}%"),
                    
                )
            ).all()
                    
            orders = list(set(searched_orders))
               
        if session.get('role') and action == 'edit': # Staff và Admin đều có quyền cập nhật trạng thái đơn hàng
            order = Order.query.filter_by(id = form.get('order_id'), admin_id = workspace_id).first()
                    
            if order:
                old_status = order.status
                new_status = form.get('status', old_status)

                if old_status == 'completed':
                    flash(_t('toast_ord_completed_err'), 'error')
                    return redirect(url_for('orders.orders_page'))
                elif old_status == 'canceled':
                    flash(_t('toast_ord_cancel_err'), 'error')
                    return redirect(url_for('orders.orders_page'))

                valid_transitions = {
                    'pending': ['pending', 'processing', 'canceled'],
                    'processing': ['processing', 'completed', 'canceled'],
                    'completed': ['completed'],
                    'canceled': ['canceled']
                }

                if new_status not in valid_transitions.get(old_status, []):
                    flash(_t('toast_ord_invalid_status'), 'error')
                    return redirect(url_for('orders.orders_page'))

                order.customer_name = form.get('customer_name', order.customer_name)
                order.customer_phone = form.get('phone', order.customer_phone)
                order.customer_email = form.get('email', order.customer_email)
                order.status = new_status
                order.shipping_address = form.get('address', order.shipping_address)
                    
                if order.status == 'canceled' and old_status != 'canceled':
                    order_items = OrderItem.query.filter_by(order_id = order.id).all()
                    restock_returned_item(order_items)
                                        
                db.session.commit()
                flash(_t('toast_ord_updated'), 'success')
                return redirect(url_for("orders.orders_page")) 

        elif session.get('role') == 'admin' and action == 'add':
            # Order
            cart_data = form.get('cart_data')
            cart_items = read_cart_data(cart_data)
            new_order = create_order(cart_items, form)
            reduce_stock(cart_items)
                
            # Order Item
            create_order_items(cart_items, new_order.id)

            flash(_t('toast_ord_created'), 'success')
            return redirect(url_for('orders.orders_page'))

    products = Product.query.filter_by(admin_id = workspace_id).all()
    return render_template('orders.html', orders = orders, products = products, user = db.session.get(User, session.get('id')))

@orders.route("/orders/order_details/<string:order_code>")
def order_detail(order_code):
    if not 'email' in session:
        return redirect(url_for('users.login'))

    workspace_id = session.get('workspace_id')
    current_user = workspace_id

    order = Order.query.filter_by(ord = order_code, admin_id = current_user).first()
    if not order:
        abort(404)

    order_items = OrderItem.query.filter_by(order_id = order.id).all()

    return render_template('order_details.html', order = order, order_items = order_items, user = db.session.get(User, session.get('id')))
