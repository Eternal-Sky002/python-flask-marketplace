from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests
from config import api_call, api_wilayah_call

item_bp = Blueprint('item', __name__)

@item_bp.route('/items')
def list_items():
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    items_response = api_call('GET', '/items', headers=headers)
    if items_response and items_response.status_code == 401:
        flash('Sesi Anda telah habis, silakan login ulang.', 'error')
        return redirect(url_for('user.login'))
    stores_response = api_call('GET', '/stores', headers=headers)
    if stores_response and stores_response.status_code == 401:
        flash('Sesi Anda telah habis, silakan login ulang.', 'error')
        return redirect(url_for('user.login'))
    
    items = items_response.json() if items_response else []
    return render_template('item/list.html', items=items)

@item_bp.route('/items/<int:item_id>')
def view_item(item_id):
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    items_response = api_call('GET', f'/items/{item_id}', headers=headers)
    if items_response.status_code == 200:
        item = items_response.json()
        return render_template('item/detail.html', item=item)
    flash('Item not found', 'error')
    return redirect(url_for('item.list_items'))

@item_bp.route('/items/store/<int:store_id>')
def view_item_store(store_id):
    headers = {'Authorization': f'Bearer {session.get("access_token")}'}
    # Get store details
    store_response = api_call('GET', f'/stores/{store_id}', headers=headers)
    if store_response.status_code != 200:
        flash('Store not found', 'error')
        return redirect(url_for('item.list_items'))
        
    # Get store items
    items_response = api_call('GET', f'/items/stores/{store_id}', headers=headers)

    if items_response.status_code == 200:
        items = items_response.json() if items_response else []
        store = store_response.json()

        return render_template('item/store_detail.html', items=items, store=store)
    flash('Items not found', 'error')
    return redirect(url_for('item.list_items'))
