/*
CAR RENTAL DATABASE 
AUTHOR: Anton Volkov 
EMAIL:antonmivo@gmail.com
PHONE:+420703977471
*/
drop database volkov
begin transaction
declare @err as tinyint
set @err = 1
go

USE [volkov]
GO
/****** Object:  Table [dbo].[auta]    Script Date: 07/01/2022 00:40:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[auta](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nazev_znack] [nvarchar](30) NULL,
	[barva] [nvarchar](10) NULL,
	[id_vyrob] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[pujcka]    Script Date: 07/01/2022 00:40:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[pujcka](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[datum_pujc] [datetime] NULL,
	[id_zaka] [int] NULL,
	[id_aut] [int] NULL,
	[typ_pujc] [nvarchar](50) NULL,
UNIQUE NONCLUSTERED 
(
	[id_aut] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ucet]    Script Date: 07/01/2022 00:40:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ucet](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[cis_uc] [varchar](10) NULL,
	[banka_naz] [nvarchar](20) NULL,
	[kod_ban] [decimal](4, 0) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[vyrobce_aut]    Script Date: 07/01/2022 00:40:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vyrobce_aut](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nazev_vyrobc] [nvarchar](40) NULL,
	[sidliste] [nvarchar](40) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[zakaznik]    Script Date: 07/01/2022 00:40:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[zakaznik](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[jmeno] [nvarchar](20) NULL,
	[prijmeni] [nvarchar](20) NULL,
	[id_uc] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[auta]  WITH CHECK ADD FOREIGN KEY([id_vyrob])
REFERENCES [dbo].[vyrobce_aut] ([id])
GO
ALTER TABLE [dbo].[pujcka]  WITH CHECK ADD FOREIGN KEY([id_aut])
REFERENCES [dbo].[auta] ([id])
GO
ALTER TABLE [dbo].[pujcka]  WITH CHECK ADD FOREIGN KEY([id_zaka])
REFERENCES [dbo].[zakaznik] ([id])
GO
ALTER TABLE [dbo].[zakaznik]  WITH CHECK ADD FOREIGN KEY([id_uc])
REFERENCES [dbo].[ucet] ([id])
GO
ALTER TABLE [dbo].[pujcka]  WITH CHECK ADD  CONSTRAINT [nespravny_typ_pujc] CHECK  (([typ_pujc]='dlouhodoba' OR [typ_pujc]='mesicni' OR [typ_pujc]='tydenni' OR [typ_pujc]='denni'))
GO
ALTER TABLE [dbo].[pujcka] CHECK CONSTRAINT [nespravny_typ_pujc]
GO
/****** Object:  StoredProcedure [dbo].[Promena_Aut]    Script Date: 07/01/2022 00:40:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[Promena_Aut](@id1 int,@id2 int) 
as 
declare @id_aut1 as int 
declare @id_aut2 as int
declare @@err as bit
begin transaction
if (@id1 not in (select id_aut from pujcka) or @id2 not in (select id_aut from pujcka))
set @@err = 1
select @id_aut1 = id_aut from [pujcka] where id = @id1
select @id_aut2 = id_aut from [pujcka] where id = @id2
update [pujcka] set id_aut = NULL where id = @id1
update [pujcka] set id_aut = @id_aut1 where id = @id2
update [pujcka] set id_aut = @id_aut2 where id = @id1
if (@@err = 1)
rollback;
if (@@err = 0)
commit;
GO
/****** Object:  StoredProcedure [dbo].[recent_pujcka]    Script Date: 07/01/2022 00:40:27 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create procedure [dbo].[recent_pujcka]
as
select top 2 p.datum_pujc as datum, p.typ_pujc as TypPujcky, z.jmeno as pujcovatel, a.nazev_znack, a.barva
from pujcka p inner join zakaznik z 
on p.id_zaka = z.id 
inner join auta a 
on p.id_aut = a.id
order by p.id desc 
GO

set @err = 0

if (@err = 1)
rollback;
if (@err = 0)
commit;