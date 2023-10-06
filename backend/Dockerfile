FROM mcr.microsoft.com/dotnet/sdk:5.0-windowsservercore-ltsc2019 AS build

# Create directory for the app source code
RUN mkdir -p /usr/src/books
WORKDIR /usr/src/books

# Copy the source and restore dependencies
COPY . /usr/src/books
RUN dotnet restore

# Expose the port and start the app
EXPOSE 5000
CMD [ "dotnet", "run" ]