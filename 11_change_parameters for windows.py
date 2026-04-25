from archicad import ACConnection
from typing import List, Tuple, Iterable
from itertools import cycle
from enum import Enum

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

################################ CONFIGURATION #################################
propertyId = acu.GetUserDefinedPropertyId("_dan_Okno", "_dan_ROLLADEN")
propertyValueString = 'Elektro Rolladen'  # Wartość, która ma być przypisana
classificationItem = acu.FindClassificationItemInSystem(
    'Klasyfikacja ARCHICAD', 'Okno')
elements = acc.GetElementsByClassification(
    classificationItem.classificationItemId)

################################################################################

# Uzyskanie identyfikatora DisplayValueEnumId dla wartości 'VINYL'
vinylEnumValueId = act.DisplayValueEnumId(propertyValueString)

# Tworzenie jednej wartości właściwości dla wszystkich elementów
constantPropertyValue = act.NormalSingleEnumPropertyValue(vinylEnumValueId)


elemPropertyValues = []
for element in elements:
    try:
        # Pobranie obecnej wartości właściwości dla elementu
        currentPropertyValue = acc.GetPropertyValuesOfElements([element], [propertyId])[0].propertyValues[0].propertyValue

        # Sprawdzenie, czy 'currentPropertyValue' jest zdefiniowane oraz ma przypisaną wartość
        if currentPropertyValue and hasattr(currentPropertyValue, 'value') and currentPropertyValue.value:
            # Sprawdzenie, czy obecna wartość jest równa 'wpisz znak'
            if currentPropertyValue.value.displayValue == '.':
                elemPropertyValues.append(
                    act.ElementPropertyValue(
                        element.elementId, propertyId, constantPropertyValue
                    )
                )
                print(f"JEST GIT Element {element.elementId.guid} ma  git: {currentPropertyValue.value.displayValue}")
            else:
                print(f"Warning: Element {element.elementId.guid} ma inną wartość: {currentPropertyValue.value.displayValue}")
        else:
            print(f"Warning: Element {element.elementId.guid} ma niezdefiniowaną wartość")

    except Exception as e:
        # Zignorowanie błędu i kontynuowanie przetwarzania
        print(f"Warning: Błąd dla elementu {element.elementId.guid}, szczegóły: {e}")

# Ustawianie wartości właściwości dla wszystkich elementów
try:
    acc.SetPropertyValuesOfElements(elemPropertyValues)
except Exception as e:
    print(f"Warning: Błąd przy ustawianiu wartości dla elementów, szczegóły: {e}")

# Wypisanie wyników
try:
    newValues = acc.GetPropertyValuesOfElements(elements, [propertyId])
    elemAndValuePairs = []

    for i in range(len(newValues)):
        for v in newValues[i].propertyValues:
            try:
                # Sprawdzenie, czy wartość jest prawidłowa i ma atrybut 'value'
                if isinstance(v.propertyValue, act.UserUndefinedPropertyValue):
                    print(f"Warning: Element {elements[i].elementId.guid} ma niezdefiniowaną wartość.")
                else:
                    # Jeśli obiekt ma atrybut 'value', dodajemy go do listy
                    elemAndValuePairs.append(
                        (elements[i].elementId.guid, str(v.propertyValue.value))  # Zmieniamy na string, aby porównać
                    )
            except Exception as e:
                print(f"Warning: Błąd przy odczytywaniu wartości dla elementu {elements[i].elementId.guid}, szczegóły: {e}")

    # Sortowanie po stringowej reprezentacji wartości
    for elemAndValuePair in sorted(elemAndValuePairs, key=lambda p: p[1]):
        print(elemAndValuePair)

except Exception as e:
    print(f"Warning: Błąd przy pobieraniu wartości właściwości, szczegóły: {e}")
