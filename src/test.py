import requests

def main():
    response = requests.get('https://www.example.com')
    print('Response Status Code:', response.status_code)

if __name__ == '__main__':
    main()
