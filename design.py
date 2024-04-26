from db import *

class Design:
    def __init__(self):
        self.editButton = '''<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
  <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
</svg>
'''

    def animals_tr(self, data: list[AnimalEntity]) -> str:
        row = ""
        for record in data:
            row += f'''
            <tr>
                <td class="px-4 py-2">{record.name}</td>
                <td class="px-4 py-2">{record.specie}</td>
                <td class="px-4 py-2">{record.origin_country}</td>
                <td class="px-4 py-2">{record.birth_date}</td>
                <td class="px-4 py-2">{record.food}</td>
                <td class="px-4 py-2">{record.feeding_time}</td>
                <td class="px-4 py-2">{record.last_cleaning}</td>
                <td class="px-4 py-2">{record.caregiver_key}</td>
                <td class="px-4 py-2">{record.cage_key}</td>
                <td class="px-4 py-2 text-center align-middle">
                    <a class="intoMiddle" href="/edit/{record.id}">{self.editButton}</a>
                </td>
            </tr>
            '''
        return row
    
    def caregivers_tr(self, data: list[Caregiver]) -> str:
        row = ""
        for record in data:
            row += f'''
            <tr>
                <td class="px-4 py-2">{record.name}</td>
                <td class="px-4 py-2 tdCenter">{record.shift_days}</td>
                <td class="px-4 py-2 tdCenter">{record.shift_times}</td>
                <td class="px-4 py-2 text-center align-middle">
                    <a class="intoMiddle" href="/edit_caregiver/{record.id}">{self.editButton}</a>
                </td>
            </tr>
            '''
        return row
    
    def cages_tr(self, data: list[Cages]) -> str:
        row = ""
        for record in data:
            row += f'''
            <tr>
                <td class="px-4 py-2">{record.name}</td>
                <td class="px-4 py-2 tdCenter">{record.cleaning_days}</td>
                <td class="px-4 py-2 tdCenter">{record.cleaning_time}</td>
                <td class="px-4 py-2 text-center align-middle">
                    <a class="intoMiddle" href="/edit_cage/{record.id}">{self.editButton}</a>
                </td>
            </tr>
            '''
        return row
    
    def cages_and_caregivers(self, cagesTable, caregiversTable, animal: AnimalEntity=None):
        if animal:
            caregivers = ""
            for i in caregiversTable:
                if animal.caregiver_key == i.id:
                    caregivers += f'<option selected value="{i.id}">{i.name}</option>'
                else:
                    caregivers += f'<option value="{i.id}">{i.name}</option>'
            cages =""
            for i in cagesTable:
                if animal.cage_key == i.id:
                    cages += f'<option selected value="{i.id}">{i.name}</option>'
                else:
                    cages += f'<option value="{i.id}">{i.name}</option>'
        else:
            caregivers = ""
            for i in caregiversTable:
                caregivers += f'<option value="{i.id}">{i.name}</option>'

            cages =""
            for i in cagesTable:
                cages += f'<option value="{i.id}">{i.name}</option>'
        return caregivers, cages

