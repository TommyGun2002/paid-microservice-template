# FastAPI Monetizable Microservice Template

A production-ready FastAPI template for building monetizable microservices with user authentication, subscription management, and payment processing.

## 🚀 Features

- **Authentication**: Supabase integration for user management and JWT authentication
- **Payments**: Stripe integration for subscriptions and usage-based billing
- **Authorization**: Multi-tier access control (free, premium, admin)
- **Rate Limiting**: Redis-based rate limiting with configurable limits
- **Usage Tracking**: Built-in usage metering for API calls and data processing
- **Exception Handling**: Comprehensive error handling with custom exception types
- **Docker Ready**: Complete Docker setup with Redis for production deployment
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Type Safety**: Full type hints with Pydantic models

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Supabase account (for auth & database)
- Stripe account (for payments)
- Redis (included in Docker setup)

## 🛠️ Quick Start

### 1. Clone the Template

```bash
git clone <your-repo-url> my-monetizable-api
cd my-monetizable-api
```

### 2. Environment Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 3. Configure Environment Variables

Edit `.env` with your credentials:

```env
# App Configuration
PROJECT_NAME="Your Monetizable API"
VERSION="1.0.0"

# Supabase Configuration (get from supabase.com)
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# Stripe Configuration (get from stripe.com)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Redis Configuration
REDIS_URL=redis://localhost:6379

# Security & Rate Limiting
RATE_LIMIT_PER_MINUTE=60
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
```

### 4. Set Up Database

Follow the instructions in [`docs/database-schema.md`](docs/database-schema.md) to set up your Supabase database.

### 5. Run the Application

**Option A: Local Development**
```bash
python -m uvicorn app.main:app --reload
```

**Option B: Docker (Recommended)**
```bash
docker-compose up --build
```

**Access your API:**
- API: http://localhost:8000
- Documentation: http://localhost:8000/api/v1/docs
- Health Check: http://localhost:8000/health

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/profile` - Get user profile
- `PUT /api/v1/auth/profile` - Update user profile

### Payments & Subscriptions
- `POST /api/v1/payments/create-subscription` - Create new subscription
- `POST /api/v1/payments/cancel-subscription` - Cancel subscription
- `GET /api/v1/payments/subscription-status` - Get subscription status
- `POST /api/v1/payments/webhook` - Stripe webhook handler

### Protected Features
- `GET /api/v1/protected/free-feature` - Available to all authenticated users
- `GET /api/v1/protected/premium-feature` - Requires premium subscription
- `POST /api/v1/protected/usage-tracked-feature` - Tracks usage for billing

### Admin Functions
- `GET /api/v1/admin/users` - List all users (admin only)
- `GET /api/v1/admin/subscriptions` - Subscription analytics (admin only)
- `POST /api/v1/admin/users/{user_id}/subscription` - Modify user subscription (admin only)

## 💳 Monetization Models

This template supports multiple monetization strategies:

### 1. Freemium Model
- Free tier with limited features/usage
- Premium tier with advanced features
- Configurable usage limits per plan

### 2. Subscription-Based
- Monthly/yearly recurring billing
- Multiple subscription tiers
- Automatic subscription management

### 3. Usage-Based Billing
- Pay-per-API-call pricing
- Pay-per-data-processed pricing
- Real-time usage tracking and billing

### 4. Hybrid Model
- Base subscription fee + usage charges
- Example: $10/month + $0.01 per API call over 1000

## 🏗️ Architecture

```
app/
├── api/v1/endpoints/     # API route handlers
├── core/                 # Configuration and dependencies
├── middleware/           # Custom middleware (rate limiting, etc.)
├── models/              # Pydantic data models
├── services/            # Business logic (Supabase, Stripe)
└── main.py              # FastAPI application setup
```

### Key Components

- **Supabase Service**: Handles authentication and user data
- **Stripe Service**: Manages payments and subscriptions
- **Rate Limiting**: Redis-based request limiting
- **Usage Tracking**: Automatic metering for billing
- **Exception Handling**: Standardized error responses

## 🔒 Security Features

- JWT-based authentication via Supabase
- Row Level Security (RLS) for database access
- Rate limiting to prevent abuse
- CORS configuration for web security
- Input validation with Pydantic
- Secure environment variable handling

## 🚀 Deployment

### Docker Production Deployment

1. Update environment variables for production
2. Set up your domain and SSL certificates
3. Deploy with Docker Compose:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Environment-Specific Configs

- **Development**: Local Redis, debug mode enabled
- **Production**: Redis cluster, optimized for performance
- **Testing**: In-memory Redis, test database

## 📈 Monitoring & Analytics

The template includes built-in tracking for:
- API usage metrics
- Subscription status changes
- Payment events
- Error rates and performance
- User activity patterns

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Test with Docker
docker-compose exec app pytest
```

## 📖 Customization Guide

### Adding New Endpoints

1. Create endpoint file in `app/api/v1/endpoints/`
2. Add route to `app/api/v1/router.py`
3. Implement business logic in `app/services/`

### Adding New Subscription Plans

1. Create plans in Stripe Dashboard
2. Update `app/models/subscription.py`
3. Add plan logic to `app/services/stripe_service.py`

### Custom Rate Limiting

Modify `app/middleware/rate_limiting.py` to implement:
- Per-user rate limits
- Endpoint-specific limits
- Plan-based limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions and support:
- Check the [documentation](docs/)
- Review [database schema](docs/database-schema.md)
- Open an issue on GitHub

## 🎯 Next Steps

After setting up the template:

1. Configure your Supabase project and database
2. Set up your Stripe products and pricing
3. Customize the API endpoints for your use case
4. Add your business logic
5. Test the payment flow
6. Deploy to production

Happy building! 🚀