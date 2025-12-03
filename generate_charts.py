import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 10

# Create charts directory
os.makedirs('charts', exist_ok=True)

# Load data
print("Loading data...")
df = pd.read_csv('umico_products.csv')

# Clean data
df['retail_price'] = pd.to_numeric(df['retail_price'], errors='coerce')
df['old_price'] = pd.to_numeric(df['old_price'], errors='coerce')
df['discount_percent'] = pd.to_numeric(df['discount_percent'], errors='coerce')
df['seller_rating'] = pd.to_numeric(df['seller_rating'], errors='coerce')
df['rating_value'] = pd.to_numeric(df['rating_value'], errors='coerce')
df['max_installment_months'] = pd.to_numeric(df['max_installment_months'], errors='coerce')

print(f"Total products: {len(df)}")

# ============================================================================
# 1. Top 15 Brands by Product Count
# ============================================================================
print("\n1. Generating Top Brands chart...")
brand_counts = df['brand'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(12, 8))
colors = sns.color_palette("viridis", len(brand_counts))
bars = ax.barh(range(len(brand_counts)), brand_counts.values, color=colors)
ax.set_yticks(range(len(brand_counts)))
ax.set_yticklabels(brand_counts.index)
ax.set_xlabel('Number of Products', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Brands by Product Count', fontsize=14, fontweight='bold', pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, brand_counts.values)):
    ax.text(value + 20, i, f'{value:,}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/01_top_brands.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/01_top_brands.png")

# ============================================================================
# 2. Price Distribution by Top Categories
# ============================================================================
print("\n2. Generating Price Distribution by Category chart...")
top_categories = df['category_name'].value_counts().head(8).index
df_top_cat = df[df['category_name'].isin(top_categories)]
df_top_cat = df_top_cat[df_top_cat['retail_price'] < 2000]  # Filter outliers

fig, ax = plt.subplots(figsize=(14, 8))
positions = range(len(top_categories))
data_to_plot = [df_top_cat[df_top_cat['category_name'] == cat]['retail_price'].dropna()
                for cat in top_categories]

bp = ax.boxplot(data_to_plot, positions=positions, patch_artist=True, widths=0.6,
                showfliers=False)

# Color boxes
colors = sns.color_palette("Set2", len(top_categories))
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax.set_xticks(positions)
ax.set_xticklabels([cat[:30] + '...' if len(cat) > 30 else cat
                     for cat in top_categories], rotation=45, ha='right')
ax.set_ylabel('Price (AZN)', fontsize=12, fontweight='bold')
ax.set_title('Price Distribution by Top 8 Categories (Price < 2000 AZN)',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('charts/02_price_by_category.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/02_price_by_category.png")

# ============================================================================
# 3. Discount Distribution Analysis
# ============================================================================
print("\n3. Generating Discount Distribution chart...")
df_discounted = df[df['discount_percent'] > 0]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Histogram
ax1.hist(df_discounted['discount_percent'], bins=30, color='coral',
         edgecolor='black', alpha=0.7)
ax1.axvline(df_discounted['discount_percent'].mean(), color='red',
            linestyle='--', linewidth=2, label=f'Mean: {df_discounted["discount_percent"].mean():.1f}%')
ax1.set_xlabel('Discount Percentage', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Products', fontsize=12, fontweight='bold')
ax1.set_title('Discount Distribution', fontsize=13, fontweight='bold')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Discount ranges
discount_ranges = pd.cut(df_discounted['discount_percent'],
                         bins=[0, 10, 20, 30, 40, 50, 100],
                         labels=['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50%+'])
range_counts = discount_ranges.value_counts().sort_index()

bars = ax2.bar(range(len(range_counts)), range_counts.values,
               color=sns.color_palette("Reds_r", len(range_counts)),
               edgecolor='black', alpha=0.8)
ax2.set_xticks(range(len(range_counts)))
ax2.set_xticklabels(range_counts.index, rotation=0)
ax2.set_xlabel('Discount Range', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Products', fontsize=12, fontweight='bold')
ax2.set_title('Products by Discount Range', fontsize=13, fontweight='bold')

# Add value labels
for i, (bar, value) in enumerate(zip(bars, range_counts.values)):
    ax2.text(i, value + 50, f'{value:,}', ha='center', fontweight='bold')

ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('charts/03_discount_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/03_discount_distribution.png")

# ============================================================================
# 4. Top 15 Sellers by Product Count
# ============================================================================
print("\n4. Generating Top Sellers chart...")
seller_counts = df['seller_name'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(12, 8))
colors = sns.color_palette("rocket", len(seller_counts))
bars = ax.barh(range(len(seller_counts)), seller_counts.values, color=colors)
ax.set_yticks(range(len(seller_counts)))
ax.set_yticklabels(seller_counts.index)
ax.set_xlabel('Number of Products', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Sellers by Product Count', fontsize=14, fontweight='bold', pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, seller_counts.values)):
    ax.text(value + 5, i, f'{value:,}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/04_top_sellers.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/04_top_sellers.png")

# ============================================================================
# 5. Price Range Analysis
# ============================================================================
print("\n5. Generating Price Range Analysis chart...")
price_ranges = pd.cut(df['retail_price'],
                      bins=[0, 50, 100, 200, 500, 1000, 25000],
                      labels=['0-50', '50-100', '100-200', '200-500', '500-1000', '1000+'])
range_counts = price_ranges.value_counts().sort_index()

fig, ax = plt.subplots(figsize=(12, 7))
colors = sns.color_palette("mako", len(range_counts))
bars = ax.bar(range(len(range_counts)), range_counts.values,
              color=colors, edgecolor='black', alpha=0.8)
ax.set_xticks(range(len(range_counts)))
ax.set_xticklabels([f'{label} AZN' for label in range_counts.index], rotation=0)
ax.set_xlabel('Price Range', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Products', fontsize=12, fontweight='bold')
ax.set_title('Product Distribution by Price Range', fontsize=14, fontweight='bold', pad=20)

# Add value labels and percentages
total = range_counts.sum()
for i, (bar, value) in enumerate(zip(bars, range_counts.values)):
    percentage = (value / total) * 100
    ax.text(i, value + 100, f'{value:,}\n({percentage:.1f}%)',
            ha='center', va='bottom', fontweight='bold')

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/05_price_ranges.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/05_price_ranges.png")

# ============================================================================
# 6. Seller Rating Distribution
# ============================================================================
print("\n6. Generating Seller Rating Distribution chart...")
fig, ax = plt.subplots(figsize=(12, 7))

rating_counts = df['seller_rating'].value_counts().sort_index()
bars = ax.bar(rating_counts.index, rating_counts.values,
              color=sns.color_palette("YlGn", len(rating_counts)),
              edgecolor='black', alpha=0.8, width=2)

ax.set_xlabel('Seller Rating', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Products', fontsize=12, fontweight='bold')
ax.set_title('Product Distribution by Seller Rating', fontsize=14, fontweight='bold', pad=20)

# Add mean line
mean_rating = df['seller_rating'].mean()
ax.axvline(mean_rating, color='red', linestyle='--', linewidth=2,
           label=f'Average Rating: {mean_rating:.1f}')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('charts/06_seller_ratings.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/06_seller_ratings.png")

# ============================================================================
# 7. Installment Options Analysis
# ============================================================================
print("\n7. Generating Installment Options chart...")
installment_data = df[df['installment_enabled'] == True]['max_installment_months'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(12, 7))
colors = sns.color_palette("coolwarm", len(installment_data))
bars = ax.bar(range(len(installment_data)), installment_data.values,
              color=colors, edgecolor='black', alpha=0.8)

ax.set_xticks(range(len(installment_data)))
ax.set_xticklabels([f'{int(months)} mo' for months in installment_data.index])
ax.set_xlabel('Maximum Installment Period', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Products', fontsize=12, fontweight='bold')
ax.set_title('Products by Maximum Installment Period', fontsize=14, fontweight='bold', pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, installment_data.values)):
    ax.text(i, value + 50, f'{value:,}', ha='center', fontweight='bold')

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('charts/07_installment_options.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/07_installment_options.png")

# ============================================================================
# 8. Product Ratings vs Price Scatter
# ============================================================================
print("\n8. Generating Rating vs Price Analysis chart...")
df_rated = df[(df['rating_value'] > 0) & (df['retail_price'] < 3000)].copy()

fig, ax = plt.subplots(figsize=(12, 8))
scatter = ax.scatter(df_rated['retail_price'], df_rated['rating_value'],
                    c=df_rated['rating_count'], cmap='plasma',
                    alpha=0.6, s=50, edgecolors='black', linewidth=0.5)

ax.set_xlabel('Retail Price (AZN)', fontsize=12, fontweight='bold')
ax.set_ylabel('Product Rating', fontsize=12, fontweight='bold')
ax.set_title('Product Rating vs Price (sized by review count)',
             fontsize=14, fontweight='bold', pad=20)
ax.grid(alpha=0.3)

# Add colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Number of Reviews', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_rating_vs_price.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/08_rating_vs_price.png")

# ============================================================================
# 9. Category Distribution (Top 15)
# ============================================================================
print("\n9. Generating Category Distribution chart...")
category_counts = df['category_name'].value_counts().head(15)

fig, ax = plt.subplots(figsize=(12, 9))
colors = sns.color_palette("Set3", len(category_counts))
bars = ax.barh(range(len(category_counts)), category_counts.values, color=colors,
               edgecolor='black', alpha=0.8)
ax.set_yticks(range(len(category_counts)))
ax.set_yticklabels(category_counts.index)
ax.set_xlabel('Number of Products', fontsize=12, fontweight='bold')
ax.set_title('Top 15 Product Categories', fontsize=14, fontweight='bold', pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, category_counts.values)):
    ax.text(value + 15, i, f'{value:,}', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/09_top_categories.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/09_top_categories.png")

# ============================================================================
# 10. Brand Market Share (Top 10 excluding "No Brand")
# ============================================================================
print("\n10. Generating Brand Market Analysis chart...")
brand_counts_filtered = df[df['brand'] != 'No Brand']['brand'].value_counts().head(10)
total_branded = brand_counts_filtered.sum()

fig, ax = plt.subplots(figsize=(12, 8))
colors = sns.color_palette("husl", len(brand_counts_filtered))
bars = ax.barh(range(len(brand_counts_filtered)), brand_counts_filtered.values,
               color=colors, edgecolor='black', alpha=0.8)
ax.set_yticks(range(len(brand_counts_filtered)))
ax.set_yticklabels(brand_counts_filtered.index)
ax.set_xlabel('Number of Products', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Branded Products (excluding No Brand)',
             fontsize=14, fontweight='bold', pad=20)
ax.invert_yaxis()

# Add value labels with percentages
for i, (bar, value) in enumerate(zip(bars, brand_counts_filtered.values)):
    percentage = (value / total_branded) * 100
    ax.text(value + 5, i, f'{value:,} ({percentage:.1f}%)',
            va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/10_brand_market_share.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: charts/10_brand_market_share.png")

# ============================================================================
# Generate insights summary
# ============================================================================
print("\n" + "="*70)
print("INSIGHTS SUMMARY")
print("="*70)

insights = {
    'total_products': len(df),
    'avg_price': df['retail_price'].mean(),
    'median_price': df['retail_price'].median(),
    'products_with_discount': len(df[df['discount_percent'] > 0]),
    'avg_discount': df[df['discount_percent'] > 0]['discount_percent'].mean(),
    'top_brand': df[df['brand'] != 'No Brand']['brand'].value_counts().index[0],
    'top_category': df['category_name'].value_counts().index[0],
    'avg_seller_rating': df['seller_rating'].mean(),
    'installment_enabled': len(df[df['installment_enabled'] == True]),
    'most_common_installment': df[df['installment_enabled'] == True]['max_installment_months'].mode()[0] if len(df[df['installment_enabled'] == True]) > 0 else 0,
}

print(f"\n📊 Market Overview:")
print(f"   • Total Products: {insights['total_products']:,}")
print(f"   • Average Price: {insights['avg_price']:.2f} AZN")
print(f"   • Median Price: {insights['median_price']:.2f} AZN")

print(f"\n💰 Pricing & Discounts:")
print(f"   • Products with Discounts: {insights['products_with_discount']:,} ({insights['products_with_discount']/insights['total_products']*100:.1f}%)")
print(f"   • Average Discount: {insights['avg_discount']:.1f}%")

print(f"\n🏆 Market Leaders:")
print(f"   • Top Brand: {insights['top_brand']}")
print(f"   • Top Category: {insights['top_category']}")
print(f"   • Average Seller Rating: {insights['avg_seller_rating']:.1f}/100")

print(f"\n💳 Payment Options:")
print(f"   • Products with Installments: {insights['installment_enabled']:,} ({insights['installment_enabled']/insights['total_products']*100:.1f}%)")
print(f"   • Most Common Installment: {int(insights['most_common_installment'])} months")

print("\n" + "="*70)
print("✓ All charts generated successfully in 'charts/' directory")
print("="*70)
