#!/usr/bin/env python
from aidevs import aidevs, AIDevsTask, pretty_print

TASK_NAME = "helloapi"

task = AIDevsTask(aidevs, TASK_NAME)
pretty_print("Task", task.input)
pretty_print("Hint", task.hint)
pretty_print("Answer result", task.answer(task.input.get("cookie")))
