create database XCOM

USE XCOM
Create table Product(
    ProdcutId INT IDENTITY(1,1) NOT NULL,
    ProductName VARCHAR(200) NOT NULL,
    ProductKod_xkom INT NULL,
    ProductDiscount DECIMAL(10,2) NOT NULL,
    ProductOld_price DECIMAL(10,2) NOT NULL,
    ProductNew_price DECIMAL(10,2) NOT NULL,
    ProductBefore_count INT NOT NULL,
    ProductAfter_count INT NOT NULL
)



