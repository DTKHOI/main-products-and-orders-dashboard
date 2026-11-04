from flask import render_template, session, Blueprint, redirect, url_for
from .models.models import Product, User, Order, Staff
from app import db

dashboard = Blueprint('dashboard', __name__)

@dashboard.route("/dashboard", methods=['POST', 'GET'])
def dashboard_page():
    if not 'id' in session:
        return redirect(url_for('users.login'))

    if session.get('role') != 'admin':
        return "You do not have permission to perform this action.", 403

    workspace_id = session.get('workspace_id')
    recent_orders = Order.query.filter(Order.admin_id == workspace_id).order_by(Order.created_at.desc()).limit(5)
    orders = Order.query.filter(Order.admin_id == workspace_id, Order.status == 'completed').all()

    revenue = 0
    for order in orders:
        revenue += order.total_amount

    total_prods = Product.query.filter_by(admin_id = workspace_id).count()
    active_prods = Product.query.filter_by(admin_id = workspace_id, status = 'active').count()
    low_stock_prods = Product.query.filter(Product.admin_id == workspace_id, Product.stock < 10, Product.stock >= 1).count()
    out_of_stock = Product.query.filter(Product.admin_id == workspace_id, Product.stock == 0).count()

    total_ords = Order.query.filter(Order.admin_id == workspace_id).count()
    completed_ords = Order.query.filter(Order.admin_id == workspace_id, Order.status == 'completed').count()
    processing_ords = Order.query.filter(Order.admin_id == workspace_id, Order.status == 'processing').count()
    pending_ords = Order.query.filter(Order.admin_id == workspace_id, Order.status == 'pending').count()

    total_staffs = Staff.query.filter_by(admin_id = workspace_id).count()

    return render_template('dashboard.html',
                           recent_orders = recent_orders,
                           orders = orders, 
                           revenue = revenue, 
                           total_prods = total_prods, 
                           active_prods = active_prods,
                           low_stock_prods = low_stock_prods,
                           out_of_stock = out_of_stock,
                           total_ords = total_ords,
                           completed_ords = completed_ords,
                           processing_ords = processing_ords,
                           pending_ords = pending_ords,
                           user = db.session.get(User, session.get('id')),
                           total_staffs = total_staffs
                           )