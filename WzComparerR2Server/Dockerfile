FROM mcr.microsoft.com/dotnet/aspnet:6.0-focal AS base
RUN apt-get update && apt-get install -y libgdiplus
WORKDIR /app
EXPOSE 7209

ENV ASPNETCORE_URLS="http://+:7209;http://+:5285"

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-dotnet-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

FROM mcr.microsoft.com/dotnet/sdk:6.0-focal AS build
RUN dotnet dev-certs https
WORKDIR /src
COPY ["WzComparerR2Server.csproj", "./"]
RUN dotnet restore "WzComparerR2Server.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "WzComparerR2Server.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "WzComparerR2Server.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "WzComparerR2Server.dll"]