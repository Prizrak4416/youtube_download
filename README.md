# youtube_download

Download FulHD video nad sound after combine them.
You can download audio mp3 from video.


### bug pytube in extract.py
        
<        def apply_descrambler(stream_data: Dict, key: str) -> None:
should be            
            cipher_url = [
                parse_qs(formats[i]["signatureCipher"]) for i, data in enumerate(formats)
            ]       
was
        cipher_url = [
                parse_qs(formats[i]["Cipher"]) for i, data in enumerate(formats)
            ]
>
