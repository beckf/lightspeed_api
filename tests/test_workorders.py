
from datetime import datetime
import lightspeed_api


def test_workorder_create_delete(ls_client):
    workorder = lightspeed_api.models.Workorder()
    workorder.received_time = datetime.utcnow()
    ls_client.api.add(workorder)

    try:
        workorder.save()
        assert(False)
    except Exception:
        pass

    workorder = ls_client.api.workorders.get_workorder(1)
    try:
        workorder.delete()
        assert(False)
    except Exception:
        pass


def test_workorder_item_create_delete(ls_client):
    workorder = lightspeed_api.models.WorkorderItem()
    workorder.workorder = ls_client.api.workorders.get_workorder(1)
    workorder.price = 1.0
    workorder.quantity = 1
    ls_client.api.add(workorder)

    try:
        workorder.save()
        assert(False)
    except Exception:
        pass

    workorder = ls_client.api.workorders.get_workorder_item(1)
    try:
        workorder.delete()
        assert(False)
    except Exception:
        pass


def test_workorder_line_create_delete(ls_client):
    workorder = lightspeed_api.models.WorkorderLine()
    workorder.workorder = ls_client.api.workorders.get_workorder(1)
    workorder.cost = 100.0
    workorder.quantity = 1
    workorder.hours = 1
    ls_client.api.add(workorder)

    try:
        workorder.save()
        assert(False)
    except Exception:
        pass

    workorder = ls_client.api.workorders.get_workorder_line(1)
    try:
        workorder.delete()
        assert(False)
    except Exception:
        pass


def test_workorder_all_functions(ls_client):
    obj_list = ls_client.api.workorders.all()
    assert(len(obj_list) > 0)

    obj_list = ls_client.api.workorders.all_items()
    assert(len(obj_list) > 0)

    obj_list = ls_client.api.workorders.all_lines()
    assert(len(obj_list) > 0)

    obj_list = ls_client.api.workorders.all_statuses()
    assert(len(obj_list) > 0)


def test_workorder_get_functions(ls_client):
    obj = ls_client.api.workorders.get_workorder(1)
    assert(obj is not None)

    obj = ls_client.api.workorders.get_workorder_item(1)
    assert(obj is not None)

    obj = ls_client.api.workorders.get_workorder_line(1)
    assert(obj is not None)

    obj = ls_client.api.workorders.get_workorder_status(1)
    assert(obj is not None)


def test_workorder_get_created_from_ls(ls_client):
    workorder = ls_client.api.workorders.get_workorder(1)
    assert(workorder is not None)
    assert(workorder.received_time is not None and workorder.received_time < datetime.utcnow())
    assert(workorder.estimated_out_time is not None and workorder.received_time < datetime.utcnow())
    assert(workorder.last_modified_time is not None and workorder.received_time < datetime.utcnow())
    assert(workorder.note == "Receipt note to be added here!")
    assert(not workorder.is_warrantied)
    assert(not workorder.is_taxed)
    assert(not workorder.is_archived)
    assert(workorder.hook_in == "2")
    assert(workorder.hook_out == "")
    assert(workorder.is_saving_parts)
    assert(not workorder.is_same_employee_for_all_lines)
    assert(workorder.customer is not None)
    assert(workorder.customer.id == 285)
    assert(workorder.customer.name == "Jim Bob")
    assert(workorder.discount is None)
    assert(workorder.employee is not None)
    assert(workorder.serialized_object is None)
    assert(workorder.shop is not None)
    assert(workorder.sale is None)
    assert(workorder.sale_line is not None)
    assert(workorder.status is not None)

    assert(len(workorder.items) == 1)
    for t in workorder.items:
        assert(t is not None)
        assert(t.last_modified_time is not None and t.last_modified_time < datetime.utcnow())
        assert(t.item is not None and t.item.id != 0)

    assert(len(workorder.lines) == 1)
    for t in workorder.lines:
        assert(t is not None)
        assert(t.last_modified_time is not None and t.last_modified_time < datetime.utcnow())
        assert(t.sale_line is not None and t.sale_line.id != 0)


def test_workorder_item_created_from_ls(ls_client):
    workorder = ls_client.api.workorders.get_workorder_item(1)
    assert(workorder is not None)
    assert(workorder.last_modified_time is not None and workorder.last_modified_time < datetime.utcnow())
    assert(workorder.note == "")
    assert(workorder.is_warrantied)
    assert(not workorder.is_approved)
    assert(workorder.is_taxed)
    assert(workorder.is_special_order)
    assert(workorder.workorder is not None)
    assert(workorder.workorder.id == 1)
    assert(workorder.discount is None)
    assert(workorder.item is not None)
    assert(workorder.sale is None)
    assert(workorder.employee is not None)
    assert(workorder.sale_line is not None)


def test_workorder_line_created_from_ls(ls_client):
    workorder = ls_client.api.workorders.get_workorder_line(1)
    assert(workorder is not None)
    assert(workorder.last_modified_time is not None and workorder.last_modified_time < datetime.utcnow())
    assert(workorder.note == "Labor")
    assert(workorder.hours == 1)
    assert(workorder.minutes == 0)
    assert(workorder.price_override == 0.0)
    assert(workorder.quantity == 1)
    assert(workorder.cost == 125.0)
    assert(not workorder.is_warrantied)
    assert(not workorder.is_approved)
    assert(not workorder.is_taxed)
    assert(not workorder.is_done)
    assert(workorder.workorder is not None)
    assert(workorder.workorder.id == 1)
    assert(workorder.discount is None)
    assert(workorder.item is None)
    assert(workorder.sale is None)
    assert(workorder.employee is not None)
    assert(workorder.sale_line is not None)
    assert(workorder.tax_class is not None)


def test_workorder_status_created_from_ls(ls_client):
    workorder = ls_client.api.workorders.get_workorder_status(1)
    assert(workorder is not None)
    assert(workorder.name == "Open")
    assert(workorder.sort_order == 0)
    assert(workorder.color == "")
    assert(workorder.system_value == "open")
