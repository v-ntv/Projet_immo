#Ajout des données global + ratio en Python
communes_data['prix_global'] = (communes_data['prix_appartement']+communes_data['prix_maison'])/2
communes_data['min_global'] = (communes_data['min_appartement']+communes_data['min_maison'])/2
communes_data['max_global'] = (communes_data['max_appartement']+communes_data['max_maison'])/2
communes_data['loyer_global'] = (communes_data['loyer_appartement']+communes_data['loyer_maison'])/2
communes_data['loyer_min_global'] = (communes_data['loyer_min_appartement']+communes_data['loyer_min_maison'])/2
communes_data['loyer_max_global'] = (communes_data['loyer_max_appartement']+communes_data['loyer_max_maison'])/2
communes_data['ratio_m2_apt'] = round(((communes_data['loyer_appartement']*12)/communes_data['prix_appartement'])*100,2)
communes_data['ratio_m2_msn'] = round(((communes_data['loyer_maison']*12)/communes_data['prix_maison'])*100,2)
communes_data['ratio_m2_glb'] = round(((communes_data['loyer_global']*12)/communes_data['prix_global'])*100,2)