class MenuSorter:
    @staticmethod
    def sort_menu_items(food_items, preferences):
        dietary_preference = preferences['dietary_preference']
        spice_level = preferences['spice_level']
        sweet_tooth = preferences['sweet_tooth'].lower() == 'yes'

        def sort_key(item):
            score = 0

            if dietary_preference.lower() == item[4].lower():
                score += 3

            if spice_level.lower() == item[5].lower():
                score += 2

            if sweet_tooth and item[6]:
                score += 1
            return -score

        return sorted(food_items, key=sort_key)