import uuid
import re
from django.db import models
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, resolve_url, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils.formats import number_format
from django.utils import timezone


