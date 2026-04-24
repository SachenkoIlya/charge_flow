from phonenumbers import geocoder
import phonenumbers



class NormalizePhone:
    @staticmethod
    def get_country_name(phone: str, region: str):
        parsed = phonenumbers.parse(phone, region)
        return geocoder.description_for_number(parsed, "ru")
    

    @staticmethod
    def normalize_phone(phone: str, default_region: str = 'RU'):
        try:
            parsed = phonenumbers.parse(phone, default_region)

            if not phonenumbers.is_valid_number(parsed):
                return None
            
            normalized = phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )
            country_code = parsed.country_code
            region_code = phonenumbers.region_code_for_number(parsed)


            country_name = NormalizePhone.get_country_name(normalized, region_code)
            return {
                "phone": normalized,
                'country_name': country_name,
                "country_code": country_code,   # 7
                "region_code": region_code            # RU
            }

        except phonenumbers.NumberParseException:
            return None