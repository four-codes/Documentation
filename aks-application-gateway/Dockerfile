FROM mcr.microsoft.com/dotnet/core/sdk:3.1 as build
# Passing Arguments
ARG SONAR_PROJECT_KEY=test
ARG SONAR_OGRANIZAION_KEY=sonar
ARG SONAR_HOST_URL=http://13.82.xxx.xxx:9000
ARG SONAR_TOKEN=9a3a91fbfa666ad5196ac5928bbe3adbfdc4
WORKDIR /app

# Restore NuGet packages
COPY . .

# Install Sonar Scanner, Coverlet and Java (required for Sonar Scanner)
RUN apt-get update && apt-get install default-jdk -y -qq
# RUN apt-get update && apt-get install -y openjdk-11-jdk -qq
RUN dotnet tool install --global dotnet-sonarscanner
# RUN dotnet tool install --global coverlet.console
ENV PATH="$PATH:/root/.dotnet/tools"

WORKDIR /app/BackendService2

# Start Sonar Scanner
RUN dotnet sonarscanner begin \
    /k:"$SONAR_PROJECT_KEY" \
    /d:sonar.host.url="$SONAR_HOST_URL" \
    /d:sonar.login="$SONAR_TOKEN"

RUN dotnet restore

# Build and test the application
RUN dotnet publish -c Release -r alpine-x64 --self-contained true /p:PublishTrimmed=true -o ./publish

# RUN dotnet test \
#   /p:CollectCoverage=true \
#   /p:CoverletOutputFormat=opencover \
#   /p:CoverletOutput="/coverage"

# End Sonar Scanner
RUN dotnet sonarscanner end /d:sonar.login="$SONAR_TOKEN"

FROM alpine
ENV COMPlus_EnableDiagnostic=0
RUN addgroup -S user && adduser -S user -G user
RUN apk add --no-cache libstdc++ libintl icu
RUN apk add --no-cache openssh libunwind nghttp2-libs libidn krb5-libs libuuid lttng-ust zlib libstdc++ libintl icu
WORKDIR /app
RUN rm -rf /var/cache/apk/*
# Open port
EXPOSE 8080

# Copy the build output from the SDK image
COPY --from=build /app/BackendService2/publish ./
USER user
# Start the application
ENTRYPOINT ["./BackendService2", "--urls", "http://0.0.0.0:80"]
