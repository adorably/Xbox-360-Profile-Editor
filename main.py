import json
import httpx
import base64
import tkinter
import tkinter.messagebox
from dataclasses import dataclass

class Xbox360App(tkinter.Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.width: int = 250
        self.height: int = 320

        self.__setup()
        self.__create_widgets()

    def __setup(self) -> None:
        self.geometry(f'{self.width}x{self.height}+{(self.winfo_screenwidth() // 2) - (self.width//2)}+{(self.winfo_screenheight() // 2) - (self.height // 2)}')
        self.title('Xbox 360 Profile Editor')

    def __create_widgets(self) -> None:
        self.token_label: tkinter.Label = tkinter.Label(self, text='XBL3.0 Token:')
        self.token_label.pack(pady=0)
        self.token_entry: tkinter.Entry = tkinter.Entry(self, justify='center', show='*', width=35)
        self.token_entry.pack(pady=0)

        self.gamerpicture_checked: tkinter.BooleanVar = tkinter.BooleanVar()
        self.gamerpicture_checkbox: tkinter.Checkbutton = tkinter.Checkbutton(self, text='GamerPicture URL:', variable=self.gamerpicture_checked)
        self.gamerpicture_checkbox.pack(pady=0)
        self.gamerpic_entry: tkinter.Entry = tkinter.Entry(self, justify='center', width=35)
        self.gamerpic_entry.pack(pady=0)

        self.motto_checked: tkinter.BooleanVar = tkinter.BooleanVar()
        self.motto_checkbox: tkinter.Checkbutton = tkinter.Checkbutton(self, text='Motto:', variable=self.motto_checked)
        self.motto_checkbox.pack(pady=0)
        self.motto_entry: tkinter.Entry = tkinter.Entry(self, justify='center', width=35)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           # Em <3
        self.motto_entry.pack(pady=0)

        self.location_checked: tkinter.BooleanVar = tkinter.BooleanVar()
        self.location_checkbox: tkinter.Checkbutton = tkinter.Checkbutton(self, text='Location:', variable=self.location_checked)
        self.location_checkbox.pack(pady=0)
        self.location_entry: tkinter.Entry = tkinter.Entry(self, justify='center', width=35)
        self.location_entry.pack(pady=0)

        self.bio_checked: tkinter.BooleanVar = tkinter.BooleanVar()
        self.bio_checkbox: tkinter.Checkbutton = tkinter.Checkbutton(self, text='Bio:', variable=self.bio_checked)
        self.bio_checkbox.pack(pady=0)
        self.bio_entry: tkinter.Entry = tkinter.Entry(self, justify='center', width=35)
        self.bio_entry.pack(pady=0)

        self.name_checked: tkinter.BooleanVar = tkinter.BooleanVar()
        self.name_checkbox: tkinter.Checkbutton = tkinter.Checkbutton(self, text='Name:', variable=self.name_checked)
        self.name_checkbox.pack(pady=0)
        self.name_entry: tkinter.Entry = tkinter.Entry(self, justify='center', width=35)
        self.name_entry.pack(pady=0)

        self.set_button: tkinter.Button = tkinter.Button(self, text='Set Values', command=self.__set_all, width=25)
        self.set_button.pack(pady=15)

    def __set_all(self) -> None:
        token: str = (self.token_entry.get()).strip()
        if not token:
            return tkinter.messagebox.showwarning('Token Not Set!', 'Please set an XBL3.0 Token before continuing.')

        if not any(
            [
                self.gamerpicture_checked.get(),
                self.motto_checked.get(),
                self.location_checked.get(),
                self.bio_checked.get(),
                self.name_checked.get()
            ]
        ):
            return tkinter.messagebox.showwarning('No Values Selected!', 'Please select a value to edit before continuing.')
        
        gamerpicture: str | None = None
        if self.gamerpicture_checked.get():
            gamerpicture = (self.gamerpic_entry.get()).strip()
            if not gamerpicture:
                return tkinter.messagebox.showwarning('Invalid Gamerpicture Value Set.', 'Please unselect the GamerPicture value, or set a valid value before continuing.')
        
        motto: str | None = None
        if self.motto_checked.get():
            motto = (self.motto_entry.get()).strip()
            if not motto:
                return tkinter.messagebox.showwarning('Invalid Motto Value Set.', 'Please unselect the Motto value, or set a valid value before continuing.')
        
        location: str | None = None
        if self.location_checked.get():
            location = (self.location_entry.get()).strip()
            if not location:
                return tkinter.messagebox.showwarning('Invalid Location Value Set.', 'Please unselect the Location value, or set a valid value before continuing.')
        
        bio: str | None = None
        if self.bio_checked.get():
            bio = (self.bio_entry.get()).strip()
            if not bio:
                return tkinter.messagebox.showwarning('Invalid Bio Value Set.', 'Please unselect the Bio value, or set a valid value before continuing.')
            
        name: str | None = None
        if self.name_checked.get():
            name = (self.name_entry.get()).strip()
            if not name:
                return tkinter.messagebox.showwarning('Invalid Name Value Set.', 'Please unselect the Name value, or set a valid value before continuing.')

        jobStatus: Job = XSAPI.execute(
            token=token,
            job=Job(
                SetMotto=self.motto_checked.get(),
                SetLocation=self.location_checked.get(),
                SetGamerPicture=self.gamerpicture_checked.get(),
                SetBio=self.bio_checked.get(),
                SetName=self.name_checked.get()
            ),
            gamerpicture=gamerpicture,
            motto=motto,
            location=location,
            bio=bio,
            name=name
        )

        statusInformation: str = ''

        if jobStatus.SetGamerPicture:
            statusInformation += f'Public Gamerpic: {"Success" if jobStatus.GamerPicturePublicStatus else "Failure"}\n'
            statusInformation += f'Personal Gamerpic: {"Success" if jobStatus.GamerPicturePublicStatus else "Failure"}\n'
            statusInformation += f'Xbox One Gamerpic: {"Success" if jobStatus.GamerPicturePublicStatus else "Failure"}\n'
        
        if jobStatus.SetMotto:
            statusInformation += f'Motto: {"Success" if jobStatus.MottoStatus else "Failure"}\n'
        
        if jobStatus.SetLocation:
            statusInformation += f'Location: {"Success" if jobStatus.LocationStatus else "Failure"}\n'
        
        if jobStatus.SetBio:
            statusInformation += f'Bio: {"Success" if jobStatus.BioStatus else "Failure"}\n'
        
        if jobStatus.SetName:
            statusInformation += f'Name: {"Success" if jobStatus.NameStatus else "Failure"}\n'

        tkinter.messagebox.showinfo(title='All Values Sent.', message=statusInformation)

@dataclass
class Job:
    SetMotto: bool = False
    MottoStatus: bool = False

    SetBio: bool = False
    BioStatus: bool = False

    SetGamerPicture: bool = False
    GamerPicturePublicStatus: bool = False
    GamerPicturePersonalStatus: bool = False
    GamerPictureXboxOneStatus: bool = False
    
    SetName: bool = False
    NameStatus: bool = False

    SetLocation: bool = False
    LocationStatus: bool = False

class XSAPI:
    __XPROFILE_GAMERCARD_USER_MOTTO__       :int = 1076625425
    __XPROFILE_GAMERCARD_USER_LOCATION__    :int = 1079115841
    __XPROFILE_GAMERCARD_USER_NAME__        :int = 1090781248
    __XPROFILE_GAMERCARD_USER_BIO__         :int = 1139277891
    __XPROFILE_GAMERCARD_PICTURE_KEY__      :int = 1080295439
    __XPROFILE_GAMERCARD_PERSONAL_PICTURE__ :int = 1080295440
    
    __PUBLIC_GAMERPIC_KEY__: str = 'PublicGamerpic'

    __360_USER_SETTING__: dict = {
        'userSetting': {
            'id': '',
            'source': '0',
            'titleId': '4294838225',
            'value': ''
        }
    }

    __USER_SETTING__: dict = {
        'userSetting': {
            'id': '',
            'value': ''
        }
    }

    @classmethod
    def execute(
        cls, 
        token: str,
        job: Job,
        gamerpicture: str | None = None,
        motto: str | None = None,
        location: str | None = None,
        bio: str | None = None,
        name: str | None = None
    ) -> None:
        
        with httpx.Client(verify=False, timeout=30) as session:

            if job.SetGamerPicture:
                cls.__set_gamerpicture(session=session, token=token, uri=gamerpicture, job=job)
            
            if job.SetMotto:
                cls.__set_motto(session=session, token=token, content=motto, job=job)

            if job.SetName:
                cls.__set_name(session=session, token=token, content=name, job=job)

            if job.SetBio:
                cls.__set_bio(session=session, token=token, content=bio, job=job)

            if job.SetLocation:
                cls.__set_location(session=session, token=token, content=location, job=job)
        
        return job
    
    @classmethod
    def __set_gamerpicture(cls, session: httpx.Client, token: str, uri: str, job: Job) -> None:
        value: str = cls.__get_gamerpicture_value(value=uri)
        if not value:
            print('Invalid Picture URL.')
            job.GamerPicturePublicStatus = False
            job.GamerPicturePersonalStatus = False
            job.GamerPictureXboxOneStatus = False
            return 

        payload: dict = cls.__360_USER_SETTING__.copy()
        payload['userSetting']['id'] = str(cls.__XPROFILE_GAMERCARD_PICTURE_KEY__)
        payload['userSetting']['value'] = value 

        job.GamerPicturePublicStatus = cls.__parse_settings(session=session, token=token, user_setting=payload, setting=str(cls.__XPROFILE_GAMERCARD_PICTURE_KEY__))
    
        payload['userSetting']['id'] = str(cls.__XPROFILE_GAMERCARD_PERSONAL_PICTURE__)

        job.GamerPicturePersonalStatus = cls.__parse_settings(session=session, token=token, user_setting=payload, setting=str(cls.__XPROFILE_GAMERCARD_PICTURE_KEY__))

        payload: dict = cls.__USER_SETTING__.copy()
        payload['userSetting']['id'] = cls.__PUBLIC_GAMERPIC_KEY__

        job.GamerPictureXboxOneStatus = cls.__parse_settings(session=session, token=token, user_setting=payload, setting=cls.__PUBLIC_GAMERPIC_KEY__, contract='2')

    @classmethod
    def __set_motto(cls, session: httpx.Client, token: str, content: str, job: Job) -> None:
        value: str = cls.__get_content_value(content=content)
        if not value:
            job.MottoStatus = False
            return
        
        payload: dict = cls.__360_USER_SETTING__.copy()
        payload['userSetting']['id'] = str(cls.__XPROFILE_GAMERCARD_USER_MOTTO__)
        payload['userSetting']['value'] = value

        job.MottoStatus = cls.__parse_settings(session=session, token=token, user_setting=payload, setting=str(cls.__XPROFILE_GAMERCARD_USER_MOTTO__))
    
    @classmethod
    def __set_name(cls, session: httpx.Client, token: str, content: str, job: Job) -> None:
        value: str = cls.__get_content_value(content=content)
        if not value:
            job.NameStatus = False
            return
        
        payload: dict = cls.__360_USER_SETTING__.copy()
        payload['userSetting']['id'] = str(cls.__XPROFILE_GAMERCARD_USER_NAME__)
        payload['userSetting']['value'] = value

        job.NameStatus = cls.__parse_settings(session=session, token=token, user_setting=payload, setting=str(cls.__XPROFILE_GAMERCARD_USER_NAME__))
    
    @classmethod
    def __set_bio(cls, session: httpx.Client, token: str, content: str, job: Job) -> None:
        value: str = cls.__get_content_value(content=content)
        if not value:
            job.BioStatus = False
            return
        
        payload: dict = cls.__360_USER_SETTING__.copy()
        payload['userSetting']['id'] = str(cls.__XPROFILE_GAMERCARD_USER_BIO__)
        payload['userSetting']['value'] = value

        job.BioStatus = cls.__parse_settings(session=session, token=token, user_setting=payload, setting=str(cls.__XPROFILE_GAMERCARD_USER_BIO__))

    @classmethod
    def __set_location(cls, session: httpx.Client, token: str, content: str, job: Job) -> None:
        value: str = cls.__get_content_value(content=content)
        if not value:
            job.LocationStatus = False
            return
        
        payload: dict = cls.__360_USER_SETTING__.copy()
        payload['userSetting']['id'] = str(cls.__XPROFILE_GAMERCARD_USER_LOCATION__)
        payload['userSetting']['value'] = value

        job.LocationStatus = cls.__parse_settings(session=session, token=token, user_setting=payload, setting=str(cls.__XPROFILE_GAMERCARD_USER_LOCATION__))
    
    @classmethod
    def __get_gamerpicture_value(cls, value: str) -> str | None:
        try:
            if 'xboxgamer.pics' in value:
                [title, contentId] = value.split('titles/', 1)[1].split('/')
                contentId = contentId.rstrip('.png')
            else:
                [title, _, _, contentId] = value.split('t.', 1)[1].split('/')
            raw: bytes = b''
            raw += title.encode('UTF-16LE')
            raw += '000'.encode('UTF-16LE')
            raw += contentId.encode('UTF-16LE')
            raw += '000'.encode('UTF-16LE')
            raw += f'1{contentId[1:]}'.encode('UTF-16LE')
            raw += b'\x00\x00'
            return base64.b64encode(bytearray.fromhex(raw.hex())).decode()
        except:
            return None
        
    @classmethod
    def __get_content_value(cls, content: str) -> str | None:
        try:
            raw: bytes = b''
            raw += content.encode('UTF-16LE')
            raw += b'\x00\x00'
            return base64.b64encode(bytearray.fromhex(raw.hex())).decode()
        except:
            return None
    
    @classmethod
    def __parse_settings(cls, session: httpx.Client, token: str, user_setting: dict, setting: str, contract: str = '1') -> bool:
        try:
            r: httpx.Response = session.post(
                f'https://profile.xboxlive.com/users/me/profile/settings/{setting}',
                headers = {
                    'Authorization': token,
                    'X-XBL-Contract-Version': contract,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
                },
                json = user_setting
            )

            #print(r.status_code, '\n', r.text)

            return r.status_code in [200, 201, 204]
        except:# Exception as e:
            #print(e)
            return False

if __name__ == '__main__':
    application: Xbox360App = Xbox360App()
    application.mainloop()