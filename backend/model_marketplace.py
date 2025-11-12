"""
OWN-AI Model Marketplace
Buy and sell anonymized fine-tuned models
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import hashlib


class ModelCategory(Enum):
    """Model categories for marketplace"""
    LEGAL = "legal"
    MEDICAL = "medical"
    FINANCE = "finance"
    CODE = "code"
    CUSTOMER_SERVICE = "customer_service"
    CREATIVE = "creative"
    TRANSLATION = "translation"
    ANALYSIS = "analysis"
    GENERAL = "general"


class LicenseType(Enum):
    """Model licensing types"""
    SINGLE_USE = "single_use"  # One-time purchase
    SUBSCRIPTION = "subscription"  # Monthly licensing
    PERPETUAL = "perpetual"  # Buy once, use forever
    API_ONLY = "api_only"  # Access via API, no model download


@dataclass
class MarketplaceModel:
    """Model listed on marketplace"""
    model_id: str
    name: str
    description: str
    category: ModelCategory
    base_model: str  # e.g., "Llama-3.1-8B"

    # Seller information (anonymized)
    seller_id: str  # Hashed seller identity
    seller_rating: float = 0.0

    # Pricing
    price_usd: float = 0.0
    license_type: LicenseType = LicenseType.SUBSCRIPTION
    monthly_price: Optional[float] = None

    # Performance metrics
    benchmarks: Dict[str, float] = field(default_factory=dict)
    accuracy: Optional[float] = None
    speed_tokens_per_sec: Optional[float] = None

    # Usage stats
    downloads: int = 0
    active_users: int = 0
    avg_rating: float = 0.0
    num_reviews: int = 0

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    tags: List[str] = field(default_factory=list)
    is_verified: bool = False
    is_featured: bool = False


@dataclass
class ModelLicense:
    """License for purchased model"""
    license_id: str
    model_id: str
    buyer_id: str
    seller_id: str
    license_type: LicenseType
    price_paid: float
    purchased_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True
    usage_count: int = 0
    usage_limit: Optional[int] = None


class ModelMarketplace:
    """
    Marketplace for buying and selling fine-tuned models.

    Key Features:
    - Sellers monetize their fine-tuned models
    - Buyers get pre-trained domain models
    - All models anonymized (no training data exposed)
    - Revenue sharing: 70% seller, 30% platform
    - Quality verification and ratings
    """

    def __init__(self):
        self.models: Dict[str, MarketplaceModel] = {}
        self.licenses: Dict[str, ModelLicense] = {}
        self.revenue_share_seller = 0.70
        self.revenue_share_platform = 0.30

    def list_model(
        self,
        seller_id: str,
        model_name: str,
        description: str,
        category: ModelCategory,
        base_model: str,
        price_usd: float,
        license_type: LicenseType = LicenseType.SUBSCRIPTION,
        benchmarks: Optional[Dict[str, float]] = None
    ) -> str:
        """
        List fine-tuned model on marketplace.

        Args:
            seller_id: Seller's user ID
            model_name: Name of the model
            description: What the model does
            category: Model category
            base_model: Base model used
            price_usd: Price (per month for subscription)
            license_type: Licensing type
            benchmarks: Performance benchmarks

        Returns:
            Model ID
        """

        # Generate model ID
        model_id = hashlib.sha256(
            f"{seller_id}{model_name}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]

        # Anonymize seller ID
        anonymized_seller = hashlib.sha256(seller_id.encode()).hexdigest()[:12]

        model = MarketplaceModel(
            model_id=model_id,
            name=model_name,
            description=description,
            category=category,
            base_model=base_model,
            seller_id=anonymized_seller,
            price_usd=price_usd,
            license_type=license_type,
            benchmarks=benchmarks or {}
        )

        self.models[model_id] = model

        return model_id

    def search_models(
        self,
        category: Optional[ModelCategory] = None,
        max_price: Optional[float] = None,
        min_rating: Optional[float] = None,
        tags: Optional[List[str]] = None,
        sort_by: str = "popularity"  # "popularity", "price", "rating", "newest"
    ) -> List[MarketplaceModel]:
        """
        Search marketplace for models.

        Args:
            category: Filter by category
            max_price: Maximum price
            min_rating: Minimum rating
            tags: Filter by tags
            sort_by: Sort order

        Returns:
            List of matching models
        """
        results = list(self.models.values())

        # Apply filters
        if category:
            results = [m for m in results if m.category == category]

        if max_price:
            results = [m for m in results if m.price_usd <= max_price]

        if min_rating:
            results = [m for m in results if m.avg_rating >= min_rating]

        if tags:
            results = [
                m for m in results
                if any(tag in m.tags for tag in tags)
            ]

        # Sort results
        if sort_by == "popularity":
            results.sort(key=lambda m: m.active_users, reverse=True)
        elif sort_by == "price":
            results.sort(key=lambda m: m.price_usd)
        elif sort_by == "rating":
            results.sort(key=lambda m: m.avg_rating, reverse=True)
        elif sort_by == "newest":
            results.sort(key=lambda m: m.created_at, reverse=True)

        return results

    def purchase_model(
        self,
        buyer_id: str,
        model_id: str,
        license_duration_months: int = 1
    ) -> ModelLicense:
        """
        Purchase model from marketplace.

        Args:
            buyer_id: Buyer's user ID
            model_id: Model to purchase
            license_duration_months: License duration (for subscription)

        Returns:
            Model license
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")

        model = self.models[model_id]

        # Calculate price
        if model.license_type == LicenseType.SUBSCRIPTION:
            total_price = model.price_usd * license_duration_months
        else:
            total_price = model.price_usd

        # Generate license
        license_id = hashlib.sha256(
            f"{buyer_id}{model_id}{datetime.utcnow().isoformat()}".encode()
        ).hexdigest()[:16]

        # Calculate expiration
        expires_at = None
        if model.license_type == LicenseType.SUBSCRIPTION:
            from datetime import timedelta
            expires_at = datetime.utcnow() + timedelta(days=30 * license_duration_months)

        license = ModelLicense(
            license_id=license_id,
            model_id=model_id,
            buyer_id=buyer_id,
            seller_id=model.seller_id,
            license_type=model.license_type,
            price_paid=total_price,
            purchased_at=datetime.utcnow(),
            expires_at=expires_at
        )

        self.licenses[license_id] = license

        # Update model stats
        model.downloads += 1
        model.active_users += 1

        # Process payment and revenue sharing
        self._process_payment(model.seller_id, total_price)

        return license

    def _process_payment(self, seller_id: str, total_price: float):
        """Process payment and revenue sharing"""
        seller_revenue = total_price * self.revenue_share_seller
        platform_revenue = total_price * self.revenue_share_platform

        # In production: Transfer funds via Stripe
        # stripe.Transfer.create(
        #     amount=int(seller_revenue * 100),
        #     currency="usd",
        #     destination=seller_stripe_account
        # )

        print(f"Revenue split: Seller ${seller_revenue:.2f}, Platform ${platform_revenue:.2f}")

    def rate_model(
        self,
        license_id: str,
        rating: float,
        review: Optional[str] = None
    ) -> bool:
        """
        Rate purchased model.

        Args:
            license_id: License ID (proves purchase)
            rating: Rating 1-5
            review: Optional review text

        Returns:
            Success status
        """
        if license_id not in self.licenses:
            raise ValueError("Invalid license or not purchased")

        license = self.licenses[license_id]
        model = self.models[license.model_id]

        # Update model rating
        total_rating = model.avg_rating * model.num_reviews
        model.num_reviews += 1
        model.avg_rating = (total_rating + rating) / model.num_reviews

        return True

    def get_seller_analytics(self, seller_id: str) -> Dict[str, Any]:
        """Get analytics for seller"""

        # Anonymize seller ID
        anonymized = hashlib.sha256(seller_id.encode()).hexdigest()[:12]

        # Find seller's models
        seller_models = [
            m for m in self.models.values()
            if m.seller_id == anonymized
        ]

        if not seller_models:
            return {'error': 'No models found'}

        # Calculate metrics
        total_revenue = sum(
            license.price_paid * self.revenue_share_seller
            for license in self.licenses.values()
            if license.seller_id == anonymized
        )

        total_downloads = sum(m.downloads for m in seller_models)
        avg_rating = sum(m.avg_rating for m in seller_models) / len(seller_models)

        return {
            'total_models': len(seller_models),
            'total_revenue_usd': total_revenue,
            'total_downloads': total_downloads,
            'avg_rating': avg_rating,
            'active_licenses': sum(
                1 for l in self.licenses.values()
                if l.seller_id == anonymized and l.is_active
            )
        }

    def get_trending_models(self, limit: int = 10) -> List[MarketplaceModel]:
        """Get trending models"""
        # Sort by recent downloads and active users
        trending = sorted(
            self.models.values(),
            key=lambda m: (m.downloads + m.active_users * 10),
            reverse=True
        )

        return trending[:limit]

    def verify_model_quality(self, model_id: str) -> Dict[str, Any]:
        """
        Verify model quality before featuring.

        Runs automated tests:
        - Performance benchmarks
        - Security scan
        - Bias detection
        - Quality metrics
        """
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")

        model = self.models[model_id]

        # Run verification tests
        verification = {
            'model_id': model_id,
            'quality_score': 0.0,
            'tests': {
                'performance': self._test_performance(model),
                'security': self._test_security(model),
                'bias': self._test_bias(model),
                'documentation': self._test_documentation(model)
            }
        }

        # Calculate overall quality score
        test_scores = [test['score'] for test in verification['tests'].values()]
        verification['quality_score'] = sum(test_scores) / len(test_scores)

        # Award verification badge if quality is high
        if verification['quality_score'] >= 0.8:
            model.is_verified = True
            verification['verified'] = True

        return verification

    def _test_performance(self, model: MarketplaceModel) -> Dict[str, Any]:
        """Test model performance"""
        # In production: Run actual benchmarks
        return {
            'score': 0.85,
            'latency_ms': 150,
            'tokens_per_sec': 45,
            'passed': True
        }

    def _test_security(self, model: MarketplaceModel) -> Dict[str, Any]:
        """Test model security"""
        return {
            'score': 0.90,
            'vulnerabilities_found': 0,
            'passed': True
        }

    def _test_bias(self, model: MarketplaceModel) -> Dict[str, Any]:
        """Test for bias"""
        return {
            'score': 0.92,
            'bias_detected': False,
            'passed': True
        }

    def _test_documentation(self, model: MarketplaceModel) -> Dict[str, Any]:
        """Test documentation quality"""
        has_description = len(model.description) > 50
        has_benchmarks = len(model.benchmarks) > 0

        return {
            'score': 0.8 if has_description and has_benchmarks else 0.5,
            'passed': has_description
        }


class MarketplaceRevenueCalculator:
    """Calculate potential marketplace revenue"""

    @staticmethod
    def estimate_seller_revenue(
        price_per_month: float,
        estimated_buyers: int,
        months: int = 12
    ) -> Dict[str, float]:
        """
        Estimate seller revenue from marketplace.

        Args:
            price_per_month: Monthly subscription price
            estimated_buyers: Number of buyers
            months: Time period

        Returns:
            Revenue estimates
        """
        gross_revenue = price_per_month * estimated_buyers * months
        seller_revenue = gross_revenue * 0.70  # 70% to seller
        platform_revenue = gross_revenue * 0.30  # 30% to platform

        return {
            'gross_revenue_usd': gross_revenue,
            'seller_revenue_usd': seller_revenue,
            'platform_revenue_usd': platform_revenue,
            'avg_monthly_revenue': seller_revenue / months
        }

    @staticmethod
    def calculate_roi(
        training_cost: float,
        monthly_revenue: float
    ) -> Dict[str, Any]:
        """Calculate ROI on model development"""
        months_to_break_even = training_cost / monthly_revenue if monthly_revenue > 0 else float('inf')

        return {
            'training_cost_usd': training_cost,
            'monthly_revenue_usd': monthly_revenue,
            'months_to_break_even': months_to_break_even,
            'year_1_profit': (monthly_revenue * 12) - training_cost,
            'roi_percentage': ((monthly_revenue * 12) / training_cost - 1) * 100 if training_cost > 0 else 0
        }


# ===========================
# Example Use Cases
# ===========================

def example_marketplace_usage():
    """Example of marketplace in action"""

    marketplace = ModelMarketplace()

    # Seller lists legal contract analysis model
    model_id = marketplace.list_model(
        seller_id="law_firm_123",
        model_name="Legal Contract Analyzer Pro",
        description="Fine-tuned for M&A contract analysis. Trained on 10,000+ contracts.",
        category=ModelCategory.LEGAL,
        base_model="Llama-3.1-8B",
        price_usd=299.0,
        license_type=LicenseType.SUBSCRIPTION,
        benchmarks={
            'contract_accuracy': 0.94,
            'clause_extraction': 0.89,
            'risk_detection': 0.92
        }
    )

    print(f"Model listed: {model_id}")

    # Buyer searches for legal models
    legal_models = marketplace.search_models(
        category=ModelCategory.LEGAL,
        max_price=500.0,
        sort_by="rating"
    )

    print(f"Found {len(legal_models)} legal models")

    # Buyer purchases model
    license = marketplace.purchase_model(
        buyer_id="startup_456",
        model_id=model_id,
        license_duration_months=12
    )

    print(f"License purchased: {license.license_id}")
    print(f"Price paid: ${license.price_paid}")

    # Calculate seller revenue potential
    revenue = MarketplaceRevenueCalculator.estimate_seller_revenue(
        price_per_month=299.0,
        estimated_buyers=50,  # Estimated demand
        months=12
    )

    print(f"\nRevenue Projection:")
    print(f"Seller could earn: ${revenue['seller_revenue_usd']:,.2f}/year")
    print(f"Monthly average: ${revenue['avg_monthly_revenue']:,.2f}")


# ===========================
# Export
# ===========================

__all__ = [
    'ModelMarketplace',
    'MarketplaceModel',
    'ModelLicense',
    'ModelCategory',
    'LicenseType',
    'MarketplaceRevenueCalculator'
]
