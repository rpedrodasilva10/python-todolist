# Service for adding and reading tasks (task lists).

# Objective

The focus on this project is to fix and practice new skills that i've been reading about, Docker, Containers, RESTful API's, HTTP requests with flask and object persistence with shelve.

## Usage

All responses will have the form

``` json
{
    "data": "The content of response with multiple data types",
    "message": "Description of what happened" 
}
```

## List all tasks

**Definition**

`GET /tasklists`

**Response**

- `200 OK` on success
``` json
[
    {
        "task_id": "35872",
        "description": "Do this other thing"
    },
    {
        "task_id": "33812",
        "description": "Do this other thing here" 
    }
]
```

### Adding a new task

**Definition**

`POST /tasklist`

**Arguments**

- `"task_id":int` a unique number for this task
- `"description":string` the description of the task

If a task with the given number already exists, the existing task will be overwritten.

**Response**
- `201 Created` on success
``` json
{
  "task_id": "3021",
  "description": "Do this thing"
}
```

## Show a specific task
`GET /task/<task_id>`

**Response**

- `404 Not Found` if the task does not exist
- `200 OK` on success

## Delete a task

**Definition**

`DELETE/task/<task_id>`

**Response**

- `204 Deleted` on success or if the task does not exist
