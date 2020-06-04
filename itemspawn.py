import random
from collections import OrderedDict

MINIMUM_ITEM_TO_CATEGORY_RATIO = 3


class ItemSpawn:

    categories = None
    items = None

    def __init__(self):
        self.categories = OrderedDict({})
        self.items = OrderedDict({})

    def addCategory(self, offset, size):
        self.categories[offset] = {'probability': size, 'items': 0}

    def addItem(self, offset, categoryOffset):
        result = random.normalvariate(4.0, 2.0)
        while result < 0:
            result = random.normalvariate(4.0, 2.0)

        c = self.categories[categoryOffset]
        self.items[offset] = {'category': categoryOffset, 'probability': result}
        c['items'] += 1

    def normalize(self, sizeLimit):
        while self.testSize() > sizeLimit:
            if len(self.categories) * MINIMUM_ITEM_TO_CATEGORY_RATIO > len(self.items):
                selection = random.randint(0, len(self.categories) - 1)
                i = list(self.categories.items())[selection]
                category = list(i)[0]
                j = 0
                while j < len(self.items):
                    item = list(list(self.items.items())[j])[1]
                    if category == item['category']:
                        self.items.pop(list(list(self.items.items())[j])[0])
                    else:
                        j += 1
                self.categories.pop(list(i)[0])
            else:
                selection = random.randint(0, len(self.items) - 1)
                i = list(self.items.items())[selection]
                for j in self.categories.items():
                    if list(j)[0] == list(i)[1]['category']:
                        list(j)[1]['items'] -= 1
                        list(j)[1]['probability'] *= list(j)[1]['items'] / (list(j)[1]['items'] + 1)
                        if list(j)[1]['items'] == 0:
                            self.categories.pop(list(j)[0])
                        break
                self.items.pop(list(i)[0])

        categoryTotalProbability = 0.0
        for i in self.categories:
            categoryTotalProbability += self.categories[i]['probability']

        for i in range(0, len(self.categories)):
            list(list(self.categories.items())[i])[1]['probability'] /= categoryTotalProbability
            if i != 0:
                list(list(self.categories.items())[i])[1]['probability'] += (
                    list(list(self.categories.items())[i-1])[1]['probability'])

        for i in self.categories:
            itemTotalProbability = 0.0

            for j in self.items:
                if self.items[j]['category'] == i:
                    itemTotalProbability += self.items[j]['probability']

            first = True
            last = len(self.items)
            for j in range(0, len(self.items)):
                if list(list(self.items.items())[j])[1]['category'] == i:
                    list(list(self.items.items())[j])[1]['probability'] /= itemTotalProbability
                    if first:
                        first = False
                    else:
                        list(list(self.items.items())[j])[1]['probability'] += (
                            list(list(self.items.items())[last])[1]['probability'])
                    last = j

    def testSize(self):
        offset = 0
        size = 0
        for categoryOffset in self.categories:
            if offset == categoryOffset:
                size += 2
            else:
                size += 4
            offset = categoryOffset + 1

        for itemOffset in self.items:
            if offset == itemOffset:
                size += 2
            else:
                size += 4
            offset = itemOffset + 1

        return size + 2

    def write(self, memory, entry):
        offset = 0
        for categoryOffset in self.categories:
            if offset != categoryOffset:
                memory[entry] = (categoryOffset - offset + 30000).to_bytes(2, 'little')[0].to_bytes(1, 'little')
                memory[entry + 1] = (categoryOffset - offset + 30000).to_bytes(2, 'little')[1].to_bytes(1, 'little')
                entry += 2

            memory[entry] = (round(self.categories[categoryOffset]['probability'] * 10000).
                             to_bytes(2, 'little')[0].to_bytes(1, 'little'))
            memory[entry + 1] = (round(self.categories[categoryOffset]['probability'] * 10000).
                                 to_bytes(2, 'little')[1].to_bytes(1, 'little'))
            entry += 2
            offset = categoryOffset + 1

        for itemOffset in self.items:
            if offset != itemOffset:
                memory[entry] = (itemOffset - offset + 30000).to_bytes(2, 'little')[0].to_bytes(1, 'little')
                memory[entry + 1] = (itemOffset - offset + 30000).to_bytes(2, 'little')[1].to_bytes(1, 'little')
                entry += 2

            memory[entry] = (round(self.items[itemOffset]['probability'] * 10000).
                             to_bytes(2, 'little')[0].to_bytes(1, 'little'))
            memory[entry + 1] = (round(self.items[itemOffset]['probability'] * 10000).
                                 to_bytes(2, 'little')[1].to_bytes(1, 'little'))
            entry += 2
            offset = itemOffset + 1

        memory[entry] = 0xFF.to_bytes(1, 'little')
        memory[entry + 1] = 0x76.to_bytes(1, 'little')




