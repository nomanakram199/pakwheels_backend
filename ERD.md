# Pak Wheels — Entity Relationship Diagram (ERD)

## Visual ERD (Mermaid)

```mermaid
erDiagram
    USERS ||--o{ CARS : sells
    USERS ||--o{ FAVORITES : bookmarks
    BRAND ||--o{ MODEL : contains
    MODEL ||--o{ CARS : "is_used_in"
    CARS ||--o{ CARPHOTOS : "has"
    CARS ||--o{ FAVORITES : "is_bookmarked_by"

    USERS {
        int id PK
        string email UK
        string password
        string first_name
        string last_name
        string phone_number
        string city
        boolean is_verified
        string otp
        datetime otp_expires_at
        datetime created_at
        datetime updated_at
    }

    BRAND {
        int id PK
        string name UK
        datetime created_at
    }

    MODEL {
        int id PK
        int brand_id FK
        string name
        datetime created_at
        string "UK:(brand_id, name)"
    }

    CARS {
        int id PK
        int model_id FK
        int year
        string license_plate UK
        string city
        decimal price
        string condition
        string description
        int seller_id FK
        boolean is_deleted
        datetime created_at
        datetime updated_at
    }

    CARPHOTOS {
        int id PK
        int car_id FK
        string image_url
        boolean is_primary
        int display_order
        datetime created_at
    }

    FAVORITES {
        int id PK
        int user_id FK
        int car_id FK
        datetime created_at
        string "UK:(user_id, car_id)"
    }
```

## ASCII ERD

```
┌─────────────────────┐
│      Users          │
├─────────────────────┤
│ id (PK)             │
│ email (UNIQUE)      │
│ password            │
│ first_name          │
│ last_name           │
│ phone_number        │
│ city                │
│ is_verified         │
│ otp (temp)          │
│ otp_expires_at      │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N (seller_id)
           │
           ▼
┌─────────────────────┐         ┌──────────────────┐
│      Cars           │◄────────┤ CarPhotos        │
├─────────────────────┤ 1:N     ├──────────────────┤
│ id (PK)             │         │ id (PK)          │
│ model_id (FK)       ┼───────► │ car_id (FK)      │
│ year                │         │ image_url        │
│ license_plate (UK)  │         │ is_primary       │
│ city                │         │ display_order    │
│ price               │         │ created_at       │
│ condition           │         └──────────────────┘
│ description         │
│ seller_id (FK)      │
│ is_deleted          │
│ created_at          │
│ updated_at          │
└──────────┬──────────┘
           │
           │ 1:N (car_id)
           │
           ▼
┌─────────────────────┐
│    Favorites        │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)────────┼──────────┐
│ car_id (FK)         │          │
│ created_at          │          │
│ (user_id,           │          │
│  car_id) UNIQUE     │          │
└─────────────────────┘          │
                                  │
                                  │ N:1 (user_id)
                                  │
                                  ▼
                           ┌──────────────┐
                           │    Users     │
                           └──────────────┘


         ┌──────────────────┐
         │      Brand       │
         ├──────────────────┤
         │ id (PK)          │
         │ name (UNIQUE)    │
         │ created_at       │
         └────────┬─────────┘
                  │
                  │ 1:N (brand_id)
                  │
                  ▼
         ┌──────────────────┐
         │      Model       │
         ├──────────────────┤
         │ id (PK)          │
         │ brand_id (FK)    │
         │ name             │
         │ created_at       │
         │ (brand_id, name) │
         │ UNIQUE           │
         └────────┬─────────┘
                  │
                  │ 1:N (model_id)
                  │
                  ▼
         ┌──────────────────┐
         │      Cars        │
         └──────────────────┘
```

---

## Relationships Summary

| From  | To        | Type | Via       | Notes                                  |
| ----- | --------- | ---- | --------- | -------------------------------------- |
| Users | Cars      | 1:N  | seller_id | User sells multiple cars               |
| Users | Favorites | 1:N  | user_id   | User has multiple favorites            |
| Brand | Model     | 1:N  | brand_id  | Brand has multiple models              |
| Model | Cars      | 1:N  | model_id  | Model used in multiple cars            |
| Cars  | CarPhotos | 1:N  | car_id    | Car has multiple photos                |
| Cars  | Favorites | 1:N  | car_id    | Car can be favorited by multiple users |

---

## Constraints & Uniqueness

| Table     | Constraint        | Type   | Reason                   |
| --------- | ----------------- | ------ | ------------------------ |
| Users     | email             | UNIQUE | Login identifier         |
| Brand     | name              | UNIQUE | No duplicate brands      |
| Model     | (brand_id, name)  | UNIQUE | One model name per brand |
| Favorites | (user_id, car_id) | UNIQUE | User favors car once     |

---

## Cascade Behavior (Soft Delete)

- **User deleted:** Listings (Cars) remain but marked as inactive (future)
- **Brand deleted:** Models deleted, related Cars orphaned (prevent deletion)
- **Model deleted:** Related Cars orphaned (prevent deletion via FK constraint)
- **Car deleted:** CarPhotos & Favorites remain (reference deleted car)
- **CarPhoto deleted:** No cascade

---

## Index Strategy (Performance)

| Table     | Column(s)         | Type     | Reason                 |
| --------- | ----------------- | -------- | ---------------------- |
| Cars      | seller_id         | INDEX    | Query "my cars"        |
| Cars      | is_deleted        | INDEX    | Filter public listings |
| Cars      | model_id          | FK Index | Join with Model        |
| CarPhotos | car_id            | FK Index | Query car photos       |
| Favorites | user_id           | INDEX    | Query user favorites   |
| Favorites | car_id            | INDEX    | Query car favorites    |
| Favorites | (user_id, car_id) | UNIQUE   | Prevent duplicates     |
| Model     | brand_id          | FK Index | Filter models by brand |
