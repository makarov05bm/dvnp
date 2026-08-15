FROM golang:1.21-alpine AS build
WORKDIR /src
COPY go.mod .
COPY main.go .
RUN go mod tidy && CGO_ENABLED=0 go build -o /h2c-backend .

FROM alpine:3.19
COPY --from=build /h2c-backend /h2c-backend
EXPOSE 9999
ENTRYPOINT ["/h2c-backend"]