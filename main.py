from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.toast import toast
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.expansionpanel import MDExpansionPanel,MDExpansionPanelOneLine
from kivymd.uix.label import MDLabel
import sqlite3 as sql
from kivy.network.urlrequest import UrlRequest
import json
import urllib


KV='''
<Content>:
    size_hint:1,None
    # height:"400dp"

<ButtonContainer>:
    size_hint:1,None
    height:"80dp"
    orientation:"vertical"


<LabelContainer>:
    size_hint:1,None
    height:"30dp"
    orientation:"vertical"


<CustomButton>:
    pos_hint: {"center_x": .5, "center_y": .5}

<EtatLabel>:
    pos_hint: {"center_x": .5, "center_y": .5}
    halign:"center"


BoxLayout:
    orientation:"vertical"
    MDToolbar:
        title:"Smart Device"
        left_action_items: [["home", lambda x: print()]]
        background_color:app.theme_cls.accent_color

    MDTabs:
        id:main_tabs
        on_tab_switch: app.on_tab_switch(*args)

        Tab:
            text:"wifi"
            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                GridLayout:
                    id:result
                    cols:1
                    size_hint_y:None
                    height:self.minimum_height



        Tab:
            text:"earth"
            ScrollView:
                do_scroll_x: False
                do_scroll_y: True
                GridLayout:
                    id:result_internet
                    cols:1
                    size_hint_y:None
                    height:self.minimum_height

        Tab:
            text:"settings"
            RelativeLayout:
                BoxLayout:
                    padding:'20dp'
                    spacing:'30dp'
                    orientation: 'vertical'
                    pos_hint:{"center_x":.5,"center_y":.5}
                    size_hint:1,.5

                    MDLabel:
                        text:"Parametre Reseau"
                        halign:'center'
                    MDTextField:
                        id: wifi
                        hint_text: "adresse ip serveur local"
                        helper_text: "example: http://192.168.1.30"
                        helper_text_mode: "on_focus"
                    MDTextField:
                        id:internet
                        hint_text: "adresse site internet"
                        helper_text: "adresse site web de synchronization"
                        helper_text_mode: "on_focus"

                    MDFillRoundFlatIconButton:
                        pos_hint: {"center_x": .5}
                        icon:"send"
                        text:"Sauvgarder"
                        on_release:app.saveIp()




        Tab:
            text:"reload"
            GridLayout:
                cols:2
                RelativeLayout:
                    MDFillRoundFlatIconButton:
                        pos_hint: {"center_x": .5, "center_y": .5}
                        icon:"reload"
                        text:"local"
                        on_release:app.sync_local()

                RelativeLayout:
                    MDFillRoundFlatIconButton:
                        pos_hint: {"center_x": .5, "center_y": .5}
                        icon:"download"
                        text:"internet"
                        on_release:app.sync_internet()

        Tab:
            text:"account"
            RelativeLayout:
                BoxLayout:
                    padding:'20dp'
                    spacing:'30dp'
                    orientation: 'vertical'
                    pos_hint:{"center_x":.5,"center_y":.5}
                    size_hint:1,.5

                    MDLabel:
                        text:"MON COMPTE"
                        halign:'center'
                    MDTextField:
                        id: user
                        hint_text: "Identifiant"
                        helper_text: "Votre compte sur le site"
                        helper_text_mode: "on_focus"
                    MDTextField:
                        id:password
                        hint_text: "Mot de passe"
                        password:True
                        helper_text: "veuillez saisir votre mot de passe ici"
                        helper_text_mode: "on_focus"

                    MDFillRoundFlatIconButton:
                        pos_hint: {"center_x": .5}
                        icon:"login"
                        text:"Connexion"
                        on_release:app.login()




'''
class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class CustomButton(MDFillRoundFlatIconButton):
    def data(self,data):
        self.data=data


class ButtonContainer(RelativeLayout):
    pass

class LabelContainer(RelativeLayout):
    pass


class EtatLabel(MDLabel):
    pass


class Content(GridLayout):
    cols=2
    pass

    # --------------------------BUILDING BUTTONS FOR LOCAL-----------------------------------------------------------------------
    def build_data(self,commandes):
        for id,nom,type,etat,chambre in commandes :
            container=ButtonContainer()
            et="on" if etat else "off"

            if type =="Lampe":
                button=CustomButton(text=nom+"  "+et,icon="lightbulb",id=type+'-1-'+str(id),on_release=main_app.send_commande)

                container.add_widget(button)

            if type =="Prise":
                button=CustomButton(text=nom+"  "+et,icon="flash",id=type+'-1-'+str(id),on_release=main_app.send_commande)
                container.add_widget(button)

            if type =="Rideau":
                button1=CustomButton(text=nom+"  "+et,icon="arrow-up",id=type+"-1-"+str(id),on_press=main_app.send_commande,on_release=main_app.pause)
                container.add_widget(button1)


            self.add_widget(container)

            if type =="Rideau":
                container=ButtonContainer()
                button2=CustomButton(text=nom+"  "+et,icon="arrow-down",id=type+"-2-"+str(id),on_press=main_app.send_commande,on_release=main_app.pause)
                container.add_widget(button2)
                self.add_widget(container)

            self.height=len(commandes)*80+20

# --------------------------BUILDING BUTTONS FOR INTERNET-----------------------------------------------------------------------


    def build_data_internet(self,commandes):
        for id,nom,type,etat,chambre in commandes :
            container=ButtonContainer()
            et="on" if etat else "off"

            if type =="Lampe":
                button=CustomButton(text=nom+"  "+et,icon="lightbulb",id=type+'-1-'+str(id),on_release=main_app.send_commande_internet)

                container.add_widget(button)

            if type =="Prise":
                button=CustomButton(text=nom+"  "+et,icon="flash",id=type+'-1-'+str(id),on_release=main_app.send_commande_internet)
                container.add_widget(button)

            if type =="Rideau":
                button1=CustomButton(text=nom+"  "+et,icon="arrow-up",id=type+"-1-"+str(id),on_press=main_app.send_commande_internet,on_release=main_app.pause_internet)
                container.add_widget(button1)


            self.add_widget(container)

            if type =="Rideau":
                container=ButtonContainer()
                button2=CustomButton(text=nom+"  "+et,icon="arrow-down",id=type+"-2-"+str(id),on_press=main_app.send_commande_internet,on_release=main_app.pause_internet)
                container.add_widget(button2)
                self.add_widget(container)

            self.height=len(commandes)*80+20






class MainApp(MDApp):

    def RequestFailure(self,req,result):
        toast("veuillez réessayer")
#--------------------------------------CHAMBRES--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def save_chambres(self,req,result):
        con=sql.connect('db.db')
        cur=con.cursor()
        cur.execute("""DELETE  FROM chambres""")
        con.commit()
        cur=con.cursor()

        for single in result:
            cur.execute("""INSERT INTO chambres (id,nom) VALUES (?,?)""",(single['id'],single['nom']))

        con.commit()
        con.close()


    def save_chambres_internet(self,req,result):
        con=sql.connect('db.db')
        cur=con.cursor()
        cur.execute("""DELETE  FROM chambres_internet""")
        con.commit()
        cur=con.cursor()

        for single in result:
            cur.execute("""INSERT INTO chambres_internet (id,nom) VALUES (?,?)""",(single['local_id'],single['nom']))

        con.commit()
        con.close()


    def sync_chambres(self,internet=False):
        if not internet:
            #UrlRequest(            url,                       success,           redirect,  failure,         error,             prgs, body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
            req = UrlRequest(self.local+"/chambres/api?format=json",self.save_chambres,None,self.RequestFailure,self.RequestFailure,None,None,None,8192,5)
        else:
            #UrlRequest(            url,                                         success,                    redirect,  failure,         error,             prgs, body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
            req = UrlRequest(self.internet+"/chambres/api?format=json",self.save_chambres_internet,None,self.RequestFailure,self.RequestFailure,None,None,self.headers,8192,5)

    def bdd_get_chambres(self,internet=False):
        con=sql.connect('db.db')
        cur=con.cursor()
        if not internet:
            cur.execute("""SELECT * FROM chambres""")
        else:
            cur.execute("""SELECT * FROM chambres_internet""")
        result=cur.fetchall()
        con.close()
        return result

#------------------------------------------END CHAMBRES--------------------------------------------------------------------------------------------------------------------------------------------------------------------






#--------------------------------------COMMANDES--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def save_commandes(self,req,result):
        con=sql.connect('db.db')
        cur=con.cursor()
        cur.execute("""DELETE  FROM commandes """)
        con.commit()
        cur=con.cursor()

        for single in result:
            cur.execute("""INSERT INTO commandes (id,nom,type,etat,chambre) VALUES (?,?,?,?,?)""",(single['id'],single['nom'],single['type'],single['etat'],single['chambre']))

        con.commit()
        con.close()
        self.build_local_panel()
        toast("synchronization terminé avec success")

    def save_commandes_internet(self,req,result):
        con=sql.connect('db.db')
        cur=con.cursor()
        cur.execute("""DELETE  FROM commandes_internet """)
        con.commit()
        cur=con.cursor()

        for single in result:
            cur.execute("""INSERT INTO commandes_internet (id,nom,type,etat,chambre) VALUES (?,?,?,?,?)""",(single['local_id'],single['nom'],single['type'],single['etat'],single['chambre_local']))

        con.commit()
        con.close()
        self.build_internet_panel()
        toast("synchronization terminé avec success")


    def sync_commandes(self,internet=False):
        if not internet:
            #UrlRequest(            url,                       success,           redirect,  failure,         error,             prgs, body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
            req = UrlRequest(self.local+"/chambres/commandes/api?format=json",self.save_commandes,None,self.RequestFailure,self.RequestFailure,None,None,None,8192,5)
        else:
            #UrlRequest(            url,                                          success,           redirect,  failure,         error,           prgs, body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
            req = UrlRequest(self.internet+"/chambres/commandes/api?format=json",self.save_commandes_internet,None,self.RequestFailure,self.RequestFailure,None,None,self.headers,8192,5)


    def bdd_get_commandes(self,chambre,internet=False):
        con=sql.connect('db.db')
        cur=con.cursor()
        if not internet:
            cur.execute("""SELECT * FROM commandes WHERE chambre=?""",(chambre,))
        else:
            cur.execute("""SELECT * FROM commandes_internet WHERE chambre=?""",(chambre,))
        result=cur.fetchall()
        con.close()
        return result

#------------------------------------------END COMMANDES--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------SYNCHRONIZE LOCALLY --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def sync_local(self):
        self.sync_chambres()
        self.sync_commandes()




#--------------------------------------END SYNCHRONIZE LOCALLY --------------------------------------------------------------------------------------------------------------------------------------------------------------------




#--------------------------------------SYNCHRONIZE INTERNET --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def sync_internet(self):
        self.sync_chambres(True)
        self.sync_commandes(True)




#--------------------------------------END SYNCHRONIZE INTERNET --------------------------------------------------------------------------------------------------------------------------------------------------------------------




#------------------------------------------IP ADRESSES --------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def saveIp(self):
        con=sql.connect('db.db')
        cur=con.cursor()
        cur.execute("""DELETE  FROM adresse """)
        con.commit()
        self.local=self.root.ids.wifi.text
        self.internet=self.root.ids.internet.text
        cur.execute("""INSERT INTO adresse (local,internet) VALUES (?,?)""",(self.local,self.internet))
        con.commit()
        con.close()
        toast("sauvgardé")

#------------------------------------------END IPADRESSES--------------------------------------------------------------------------------------------------------------------------------------------------------------------



#------------------------------------------INTERNET AUTHENTICATION  --------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def login_success(self,req,result):
        con=sql.connect('db.db')
        cur=con.cursor()
        cur.execute("""DELETE  FROM token """)
        con.commit()
        cur.execute("""INSERT INTO token  VALUES (?)""",(result['token'],))
        con.commit()
        con.close()
        self.headers={'Authorization': 'Token '+result['token']}
        toast("connecté avec success")


    def login_failure(self,req,result):
        toast("erreur veuillez réessayer")


    def login(self):
        headers={'Content-type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json'}
        body=urllib.parse.urlencode({'username': self.root.ids.user.text, 'password':self.root.ids.password.text })

        #UrlRequest(    url,                      success,           redirect,  failure,         error,          prgs, body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
        req = UrlRequest(self.internet+"/api-auth/",self.login_success,None,self.login_failure,self.login_failure,None,body,headers,8192,5)


#------------------------------------------END INTERNET AUTHENTICATION--------------------------------------------------------------------------------------------------------------------------------------------------------------------





#------------------------------------------SEND ORDER LOCAL--------------------------------------------------------------------------------------------------------------------------------------------------------------------



    def chalenge_pause_success(self,request,result):
        self.chalenge=self.decrypt(result)
        device_url=str(self.target_id)+'/3'
        #UrlRequest(            url,                                                                success,           redirect,  failure,         error,             prgs,body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
        req = UrlRequest(self.local+"/chambres/commande/"+device_url+"?ch="+self.chalenge,self.commande_success,None,self.RequestFailure,self.RequestFailure,None,None,None,8192,5)


    def chalenge_success(self,req,result):
        self.chalenge=self.decrypt(result)

        device_url=str(self.target_id)+'/'+self.target_commande


        #UrlRequest(            url,                                                                  success,           redirect,  failure,         error,             prgs,body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
        req = UrlRequest(self.local+"/chambres/commande/"+device_url+"?ch="+self.chalenge,self.commande_success,None,self.RequestFailure,self.RequestFailure,None,None,None,8192,5)


    def get_chalenge(self,pause=False):
        if not pause:
            #UrlRequest(            url,                                success,           redirect,  failure,         error,             prgs,body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
            req = UrlRequest(self.local+"/chambres/chalenge",self.chalenge_success,None,self.RequestFailure,self.RequestFailure,None,None,None,8192,5)
        else:
            #UrlRequest(            url,                                success,           redirect,  failure,         error,             prgs,body,hdrs, csze,timeout, method, decode, debug, file_path, ca_file,verify)
            req = UrlRequest(self.local+"/chambres/chalenge",self.chalenge_pause_success,None,self.RequestFailure,self.RequestFailure,None,None,None,8192,5)


    def send_commande(self,instance):
        self.target_id=instance.id.split('-')[2]
        self.target_type=instance.id.split('-')[0]
        self.target_commande=instance.id.split('-')[1]
        self.target_etat=instance.text.split(' ')[-1]
        self.get_chalenge()


    def commande_success(self,req,result):
        toast("action efectué")
        if "Rideau" not in self.target_type:
            new_etat= True if "off" in self.target_etat else False
            con=sql.connect('db.db')
            cur=con.cursor()
            cur.execute("""UPDATE commandes set etat=? where id=? """,(new_etat,self.target_id))
            con.commit()
            con.close()
            self.build_local_panel()





    def pause(self,instance):
        self.get_chalenge(True)



    def decrypt(self,to_decrypt):
        numbers=[int(s) for s in to_decrypt if s.isdigit()]
        crypted=''
        i=0
        for s in to_decrypt:

            crypted_char=chr(ord(s)+numbers[i])  if i % 2 ==0 else chr(ord(s)-numbers[i]*2)
            if not crypted_char.isalnum():
                crypted_char=str(ord(crypted_char))
            if numbers[i] % 2 == 0:
                crypted+=crypted_char
            else:
                crypted=crypted_char+crypted

            i+=1
            if(i==len(numbers)):
                i=0
        return crypted

#------------------------------------------END SEND ORDER LOCAL--------------------------------------------------------------------------------------------------------------------------------------------------------------------





#------------------------------------------ SEND ORDER INTERNET--------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def send_commande_internet_success(self,req,result):
        toast("Commande envoyée avec success")



    def send_commande_internet(self,instance):
        self.target_internet_id=instance.id.split('-')[2]
        self.target_internet_type=instance.id.split('-')[0]
        self.target_internet_commande=instance.id.split('-')[1]
        self.target_internet_etat=instance.text.split(' ')[-1]
        data=json.dumps({
            'local_id':self.target_internet_id,
            'commande':self.target_internet_commande
            })


        #UrlRequest(            url,                         success,                            redirect,  failure,         error,           prgs, body,hdrs,   csze,timeout, method, decode, debug, file_path, ca_file,verify)
        req = UrlRequest(self.internet+"/chambres/todo/api/",self.send_commande_internet_success,None,self.RequestFailure,self.RequestFailure,None,data,self.headers_json,8192,5)



    def pause_internet(self,instance):
        data=json.dumps({
            'local_id':self.target_internet_id,
            'commande':3
            })


        #UrlRequest(            url,                         success,                            redirect,  failure,         error,           prgs, body,hdrs,   csze,timeout, method, decode, debug, file_path, ca_file,verify)
        req = UrlRequest(self.internet+"/chambres/todo/api/",self.send_commande_internet_success,None,self.RequestFailure,self.RequestFailure,None,data,self.headers_json,8192,5)




#------------------------------------------END SEND ORDER INTERNET--------------------------------------------------------------------------------------------------------------------------------------------------------------------






#------------------------------------------BUILD CHAMBRE AND COMMANDE EXPANSION--------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # FOR LOCAL TAB

    def build_local_panel(self):
        self.root.ids.result.clear_widgets(self.root.ids.result.children)

        options=self.bdd_get_chambres()
        if(len(options)!=0):
            for id,nom in options :
                content=Content()
                content.build_data(self.bdd_get_commandes(id))
                panel=MDExpansionPanel(icon="room.png",
                content=content,
                panel_cls=MDExpansionPanelOneLine(
                    text=nom,
                ))
                self.root.ids.result.add_widget(panel)
        else:
            toast(" veuillez synchronizer ")

            # FOR INTERNET TAB
    def build_internet_panel(self):
        self.root.ids.result_internet.clear_widgets(self.root.ids.result_internet.children)

        options=self.bdd_get_chambres(True)
        if(len(options)!=0):
            for id,nom in options :
                content=Content()
                content.build_data_internet(self.bdd_get_commandes(id,True))
                panel=MDExpansionPanel(icon="room.png",
                content=content,
                panel_cls=MDExpansionPanelOneLine(
                    text=nom,
                ))
                self.root.ids.result_internet.add_widget(panel)
        else:
            toast(" veuillez synchronizer internet ")




#------------------------------------------END BUILD CHAMBRE AND COMMANDE EXPANSION--------------------------------------------------------------------------------------------------------------------------------------------------------------------


    def on_start(self):
        self.build_local_panel()
        self.build_internet_panel()
        con=sql.connect('db.db')
        cur=con.cursor()
        cur.execute("""SELECT * FROM adresse""")
        result=cur.fetchall()
        for local,internet in result:
            self.local=local
            self.root.ids.wifi.text=local
            self.internet=internet
            self.root.ids.internet.text=internet

        cur.execute("""SELECT * FROM token""")
        result=cur.fetchall()
        for token in result:
            self.headers={'Authorization': 'Token '+token[0]}
            self.headers_json={
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Token '+token[0],
            }

        con.close()



    def build(self):
        self.theme_cls.primary_palette="Blue"
        # self.theme_cls.accent_palette="Orange"
        # self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass

main_app=MainApp()
main_app.run()
