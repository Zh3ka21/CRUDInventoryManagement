from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app.reports import generate_sales_report, generate_inventory_report, ReportForm
from app import db
from app.forms.main_forms import csrf

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/sales_report', methods=['GET', 'POST'])
@login_required
def sales_report():
    form = ReportForm()
    if current_user.status != 'admin':
        flash("Not admin, not enough roots", "error")
        return redirect(url_for('home'))

    if request.method == 'POST':
        time_period = int(request.form.get('time_period', 7))
        generate_sales_report(time_period)
        
    return render_template('sales_report.html', form=form)

@reports_bp.route('/inventory_report')
@login_required
def inventory_report():
    if current_user.status == 'admin':
        # Fetch categories from database
        inventory_data = db.items.find()
        category = request.args.get('category', 'All')
        categories = list(set([item['category'] for item in inventory_data]))

        generate_inventory_report(category)  # Generate the report before rendering

        return render_template('inventory_report.html', categories=categories, category=category)
    else:
        flash("Not admin, not enough rights", "error")
        return redirect(url_for('home'))  # Assuming you have a home route

