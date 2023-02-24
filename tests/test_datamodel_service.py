from time import sleep

import pytest
from util.meshing_workflow import new_mesh_session  # noqa: F401

from ansys.api.fluent.v0 import datamodel_se_pb2
from ansys.fluent.core.services.datamodel_se import convert_path_to_se_path


@pytest.mark.dev
@pytest.mark.fluent_232
def test_event_subscription(new_mesh_session):
    session = new_mesh_session
    session.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    tags = [
        "/workflow/created/TaskObject",
        "/workflow/modified/TaskObject:TaskObject1/Arguments",
        "/workflow/deleted/TaskObject:TaskObject1",
        "/workflow/affected/TaskObject:TaskObject1",
        "/workflow/affected/TaskObject",
        "/workflow/attribute_changed/TaskObject:TaskObject1/TaskList/isActive",
        "/workflow/command_attribute_changed/InitializeWorkflow/arguments",
    ]
    request = datamodel_se_pb2.SubscribeEventsRequest()
    e1 = request.eventrequest.add(rules="workflow")
    e1.createdEventRequest.parentpath = ""
    e1.createdEventRequest.childtype = "TaskObject"
    e2 = request.eventrequest.add(rules="workflow")
    e2.modifiedEventRequest.path = "TaskObject:TaskObject1/Arguments"
    e3 = request.eventrequest.add(rules="workflow")
    e3.deletedEventRequest.path = "TaskObject:TaskObject1"
    e4 = request.eventrequest.add(rules="workflow")
    e4.affectedEventRequest.path = "TaskObject:TaskObject1"
    e5 = request.eventrequest.add(rules="workflow")
    e5.affectedEventRequest.path = ""
    e5.affectedEventRequest.subtype = "TaskObject"
    e6 = request.eventrequest.add(rules="workflow")
    e6.attributeChangedEventRequest.path = "TaskObject:TaskObject1/TaskList"
    e6.attributeChangedEventRequest.attribute = "isActive"
    e7 = request.eventrequest.add(rules="workflow")
    e7.commandAttributeChangedEventRequest.path = ""
    e7.commandAttributeChangedEventRequest.command = "InitializeWorkflow"
    e7.commandAttributeChangedEventRequest.attribute = "arguments"
    response = session.fluent_connection.datamodel_service_se.subscribe_events(request)
    assert all(
        [
            r.status == datamodel_se_pb2.STATUS_SUBSCRIBED and r.tag == t
            for r, t in zip(response.response, tags)
        ]
    )

    request = datamodel_se_pb2.UnsubscribeEventsRequest()
    request.tag.extend(tags)
    response = session.fluent_connection.datamodel_service_se.unsubscribe_events(
        request
    )
    assert all(
        [
            r.status == datamodel_se_pb2.STATUS_UNSUBSCRIBED and r.tag == t
            for r, t in zip(response.response, tags)
        ]
    )


@pytest.mark.dev
@pytest.mark.fluent_232
def test_add_on_child_created(new_mesh_session):
    meshing = new_mesh_session
    child_paths = []
    subscription = meshing.workflow.add_on_child_created(
        "TaskObject", lambda obj: child_paths.append(convert_path_to_se_path(obj.path))
    )
    assert child_paths == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    sleep(5)
    assert len(child_paths) > 0
    child_paths.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert child_paths == []


@pytest.mark.dev
@pytest.mark.fluent_232
def test_add_on_changed(new_mesh_session):
    meshing = new_mesh_session
    task_list = meshing.workflow.Workflow.TaskList
    assert isinstance(task_list(), list)
    assert len(task_list()) == 0
    data = []
    subscription = task_list.add_on_changed(lambda obj: data.append(len(obj())))
    assert data == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    sleep(5)
    assert len(data) > 0
    assert data[0] > 0
    data.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert data == []


@pytest.mark.dev
@pytest.mark.fluent_232
def test_add_on_affected(new_mesh_session):
    meshing = new_mesh_session
    data = []
    subscription = meshing.workflow.Workflow.add_on_affected(
        lambda obj: data.append(True)
    )
    assert data == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    sleep(5)
    assert len(data) > 0
    assert data[0] == True
    data.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert data == []


@pytest.mark.dev
@pytest.mark.fluent_232
def test_add_on_affected_at_type_path(new_mesh_session):
    meshing = new_mesh_session
    data = []
    subscription = meshing.workflow.add_on_affected_at_type_path(
        "TaskObject", lambda obj: data.append(True)
    )
    assert data == []
    meshing.workflow.InitializeWorkflow(WorkflowType="Watertight Geometry")
    sleep(5)
    assert len(data) > 0
    assert data[0] == True
    data.clear()
    subscription.unsubscribe()
    meshing.workflow.InitializeWorkflow(WorkflowType="Fault-tolerant Meshing")
    sleep(5)
    assert data == []