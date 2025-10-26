"""Dish category enumeration.

This module defines the available categories for dishes in restaurants.
Categories help organize menu items and facilitate filtering.
"""

from enum import StrEnum


class DishCategory(StrEnum):
    """Categories for classifying dishes.
    
    These categories represent common menu sections and dish types
    found in restaurants across Boyacá, Colombia.
    """

    # Main courses
    APPETIZER = "appetizer"  # Entradas
    MAIN_COURSE = "main_course"  # Plato principal
    SIDE_DISH = "side_dish"  # Acompañamientos
    
    # Soups and broths
    SOUP = "soup"  # Sopas
    BROTH = "broth"  # Caldos
    
    # Breakfast items
    BREAKFAST = "breakfast"  # Desayuno
    
    # Desserts and sweets
    DESSERT = "dessert"  # Postres
    PASTRY = "pastry"  # Repostería
    
    # Beverages
    BEVERAGE = "beverage"  # Bebidas
    HOT_BEVERAGE = "hot_beverage"  # Bebidas calientes
    COLD_BEVERAGE = "cold_beverage"  # Bebidas frías
    ALCOHOLIC_BEVERAGE = "alcoholic_beverage"  # Bebidas alcohólicas
    
    # Snacks
    SNACK = "snack"  # Pasabocas / Mecatos
    
    # Salads
    SALAD = "salad"  # Ensaladas
    
    # Special
    DAILY_SPECIAL = "daily_special"  # Plato del día
    COMBO = "combo"  # Combo / Menú ejecutivo
    
    # Traditional
    TRADITIONAL = "traditional"  # Platos típicos
    
    # Other
    OTHER = "other"  # Otros

