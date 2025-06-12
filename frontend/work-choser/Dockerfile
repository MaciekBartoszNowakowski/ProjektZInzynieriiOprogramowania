FROM node:20

# Git wymagany dla niektórych paczek i husky (jeśli kiedyś potrzebny)
RUN apt-get update && apt-get install -y git

WORKDIR /app

# Skopiuj package.json i package-lock.json osobno, by wykorzystać cache
COPY package*.json ./

# Zainstaluj zależności projektu (w tym lokalny expo)
RUN npm install

# Skopiuj całą resztę kodu
COPY . .

# Uruchom aplikację przez npx (czyli lokalny Expo)
CMD ["npx", "expo", "start", "--tunnel"]