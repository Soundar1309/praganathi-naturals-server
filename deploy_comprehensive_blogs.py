#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files import File
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from blogs.models import Blog, BlogCategory, BlogTag
from django.contrib.auth import get_user_model

User = get_user_model()

def deploy_comprehensive_blogs():
    """Deploy only the latest 5 comprehensive blog posts with images"""
    print("🚀 Deploying comprehensive blog posts with images...")
    
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@pragathinaturalfarm.com',
            'name': 'Admin User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    # Clear existing comprehensive blogs (keep original 5)
    print("🧹 Cleaning up existing comprehensive blogs...")
    comprehensive_titles = [
        'Organic Farming: A Complete Guide to Benefits, Types, and Why It Matters',
        'Cattle Farming: Types, Benefits, and Role in Indian Agriculture',
        'Integrated Farming: Models, Pillars, and Role in Organic Agriculture',
        'Vermicompost: Uses, Process, and Market in India',
        'Pragathi Natural Farm: Cultivating a Self-Sustaining Organic Ecosystem'
    ]
    
    # Delete existing comprehensive blogs
    deleted_count = Blog.objects.filter(title__in=comprehensive_titles).delete()[0]
    print(f"✅ Deleted {deleted_count} existing comprehensive blogs")
    
    # Get or create categories
    categories_data = [
        {'name': 'Organic Farming', 'description': 'Tips and techniques for organic farming practices'},
        {'name': 'Sustainable Living', 'description': 'Living sustainably with nature'},
        {'name': 'Health & Wellness', 'description': 'Natural health and wellness tips'},
        {'name': 'Farm Stories', 'description': 'Stories from our farm and community'},
        {'name': 'Recipes', 'description': 'Healthy recipes using organic ingredients'},
        {'name': 'Cattle Farming', 'description': 'Comprehensive guide to cattle farming'},
        {'name': 'Integrated Farming', 'description': 'Integrated farming systems and models'},
        {'name': 'Composting', 'description': 'Composting techniques and benefits'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = BlogCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories[cat_data['name']] = category
        if created:
            print(f"📁 Created category: {category.name}")
    
    # Get or create tags
    tags_data = [
        'organic', 'farming', 'sustainability', 'health', 'wellness', 
        'natural', 'environment', 'community', 'recipes', 'nutrition',
        'gardening', 'composting', 'soil-health', 'pesticide-free',
        'cattle', 'dairy', 'livestock', 'integrated-farming', 'vermicompost',
        'biodiversity', 'self-sustainable', 'pollachi', 'pragathi-farm'
    ]
    
    tags = {}
    for tag_name in tags_data:
        tag, created = BlogTag.objects.get_or_create(name=tag_name)
        tags[tag_name] = tag
        if created:
            print(f"🏷️ Created tag: {tag.name}")
    
    # Define blog images mapping
    blog_images = {
        'Organic Farming: A Complete Guide to Benefits, Types, and Why It Matters': 'blog-1.jpg',
        'Cattle Farming: Types, Benefits, and Role in Indian Agriculture': 'blog-2.jpg',
        'Integrated Farming: Models, Pillars, and Role in Organic Agriculture': 'blog-3.jpg',
        'Vermicompost: Uses, Process, and Market in India': 'blog-4.jpg',
        'Pragathi Natural Farm: Cultivating a Self-Sustaining Organic Ecosystem': 'blog-5.jpg'
    }
    
    # Create comprehensive blogs with images
    blogs_data = [
        {
            'title': 'Organic Farming: A Complete Guide to Benefits, Types, and Why It Matters',
            'summary': 'Discover everything about organic farming—its meaning, benefits, types, and advantages. Learn why organic agriculture is the future of sustainable food production.',
            'content': '''<h2>Introduction: What is Organic Farming?</h2>
            <p>In recent years, organic farming has gained worldwide attention as people look for healthier food, a cleaner environment, and better farming practices. Organic farming means growing crops and raising animals without synthetic fertilizers, pesticides, genetically modified organisms (GMOs), or harmful chemicals. Instead, it uses natural techniques such as composting, crop rotation, green manure, and biological pest control.</p>
            
            <p>Unlike conventional methods that focus on quantity, organic agriculture focuses on quality, soil health, biodiversity, and sustainability. As one farmer once said:</p>
            
            <blockquote>"When you take care of the soil, the soil takes care of you."</blockquote>
            
            <p>This method not only produces chemical-free food but also restores balance to nature.</p>
            
            <h3>Organic Farming vs Natural Farming</h3>
            <p>Many people confuse organic farming with natural farming, but they are not the same. Let's break it down simply:</p>
            
            <h4>Organic Farming</h4>
            <ul>
                <li>Uses certified organic inputs like bio-fertilizers, natural compost, and approved organic pesticides.</li>
                <li>Requires standards, certifications, and rules to sell products as "organic."</li>
                <li>Balances traditional methods with modern science.</li>
            </ul>
            
            <h4>Natural Farming</h4>
            <ul>
                <li>Goes one step further by avoiding even external organic inputs.</li>
                <li>Relies on local resources such as cow dung, cow urine, and farm waste.</li>
                <li>Believes farming should be self-sustained with zero outside dependency.</li>
            </ul>
            
            <p>In short, organic farming allows external natural inputs, while natural farming is completely self-reliant. Both are eco-friendly, but organic farming is more structured and widely accepted in the market.</p>
            
            <h3>Why is Organic Farming Very Useful?</h3>
            <p>The usefulness of organic farming is not limited to farmers—it impacts consumers, the environment, and future generations. Here's why it is so important:</p>
            
            <h4>1. Healthier Food</h4>
            <p>Organic produce is free from harmful chemicals and pesticides. This means fewer toxins in your body and better overall health.</p>
            
            <h4>2. Environmental Protection</h4>
            <p>It reduces soil and water pollution by avoiding synthetic fertilizers. It also helps in carbon sequestration, which slows down climate change.</p>
            
            <h4>3. Better Soil Health</h4>
            <p>Organic practices like crop rotation and composting enrich soil fertility, making land more productive for the long term.</p>
            
            <h4>4. Biodiversity</h4>
            <p>Organic farms encourage the growth of insects, birds, and microorganisms that are often destroyed by chemical farming.</p>
            
            <h4>5. Economic Benefits</h4>
            <p>Though the yield may be slightly lower, organic crops usually sell at higher prices, giving farmers better profit margins.</p>
            
            <p>As consumers demand safe and sustainable food, the importance of organic farming keeps growing every year.</p>
            
            <h3>What are the Four Types of Organic Farming?</h3>
            <p>Organic farming can be practiced in different ways depending on land, crops, and resources. The four major types are:</p>
            
            <h4>1. Integrated Organic Farming</h4>
            <ul>
                <li>A system where crops and livestock are managed together.</li>
                <li>Waste from one becomes input for another (e.g., animal manure for crops).</li>
            </ul>
            
            <h4>2. Pure Organic Farming</h4>
            <ul>
                <li>Strictly avoids chemical fertilizers and pesticides.</li>
                <li>Relies only on natural manures, compost, and organic sprays.</li>
            </ul>
            
            <h4>3. Integrated Green Manure Farming</h4>
            <ul>
                <li>Focuses on growing plants like sun hemp or cowpea and plowing them back into the soil.</li>
                <li>Improves soil fertility naturally.</li>
            </ul>
            
            <h4>4. Integrated Farming Systems (IFS)</h4>
            <ul>
                <li>Combines agriculture with poultry, dairy, fishery, or beekeeping.</li>
                <li>Ensures multiple sources of income and maximum resource use.</li>
            </ul>
            
            <p>Each type of organic farming has its own benefits, but the ultimate goal is always the same: healthier food and a healthier planet.</p>
            
            <h3>Organic Farming Near Me</h3>
            <p>Many people search for organic farming near me to find fresh, chemical-free produce or to connect with local farmers. Across cities and villages, organic stores, farmers' markets, and community-supported agriculture (CSA) programs are becoming popular.</p>
            
            <p>If you want to support farmers directly, you can:</p>
            <ul>
                <li>Visit local organic markets.</li>
                <li>Look for nearby certified organic farms.</li>
                <li>Join online groups that connect organic farmers with buyers.</li>
            </ul>
            
            <p>This not only gives you fresh food but also supports local farmers who are working hard to keep agriculture natural and sustainable.</p>
            
            <h3>What are the Advantages of Organic Farming?</h3>
            <p>The list of advantages is long, but here are some of the most impactful benefits:</p>
            
            <h4>1. Safer and More Nutritious Food</h4>
            <p>Organic food is fresher, tastier, and often more nutritious because it is grown in healthy soil without synthetic inputs.</p>
            
            <h4>2. Better for Farmers and Consumers</h4>
            <p>Farmers avoid harmful exposure to chemicals, while consumers enjoy chemical-free food.</p>
            
            <h4>3. Environmental Balance</h4>
            <p>Organic farming promotes soil fertility, reduces water pollution, and supports ecological balance.</p>
            
            <h4>4. Sustainable and Profitable</h4>
            <p>Though it requires effort, organic farming provides long-term sustainability with better profit margins due to premium pricing.</p>
            
            <h4>5. Global Demand</h4>
            <p>The demand for organic products is growing worldwide, opening opportunities for farmers to export and earn higher income.</p>
            
            <h3>Final Thoughts</h3>
            <p>Organic farming is not just a method of cultivation—it is a movement towards healthier living, stronger communities, and sustainable development. By choosing organic, we are investing in our health and protecting the planet for future generations.</p>
            
            <blockquote>"The future of farming is not in chemicals, but in care—for the soil, the farmer, and the consumer."</blockquote>
            
            <p>Whether you are a farmer looking to adopt eco-friendly practices or a consumer searching for clean food, organic farming has something to offer everyone.</p>
            
            <p>So, the next time you think about food, remember that organic agriculture is not only useful—it is essential.</p>
            
            <h3>FAQs About Organic Farming</h3>
            <h4>1. What is organic farming in simple words?</h4>
            <p>Organic farming is growing food without harmful chemicals, using natural methods to keep soil and crops healthy.</p>
            
            <h4>2. Is organic farming profitable for farmers?</h4>
            <p>Yes, organic products usually sell at higher prices, giving farmers better profits despite slightly lower yields.</p>
            
            <h4>3. How is organic farming different from natural farming?</h4>
            <p>Organic farming allows certified natural inputs, while natural farming avoids all external inputs and depends only on local resources.</p>''',
            'category': categories['Organic Farming'],
            'tags': [tags['organic'], tags['farming'], tags['sustainability'], tags['soil-health'], tags['pesticide-free']],
            'featured': True,
            'status': 'published',
            'image': 'blog-1.jpg'
        },
        {
            'title': 'Cattle Farming: Types, Benefits, and Role in Indian Agriculture',
            'summary': 'Learn everything about cattle farming—its types, benefits, and importance in India. Discover how cattle farming supports sustainable agriculture and rural livelihoods.',
            'content': '''<h2>Introduction: What is Cattle Farming?</h2>
            <p>Cattle farming is one of the oldest and most important practices in rural life. It involves raising cows, buffaloes, oxen, and bulls for milk, meat, hides, and draught power. For many families, especially in India, cattle are not just animals—they are wealth, livelihood, and part of tradition.</p>
            
            <p>At its core, cattle farming is more than food production. It is also a way of ensuring sustainable agriculture, as cattle provide manure for soil health, help in ploughing fields, and support integrated farming systems.</p>
            
            <blockquote>"A cow in the field is not just an animal—it is a partner in farming."</blockquote>
            
            <h3>Types of Cattle Farming</h3>
            <p>Cattle farming can be divided into different categories based on purpose and method. Here are the major types:</p>
            
            <h4>1. Dairy Farming</h4>
            <p>This type focuses on raising cows and buffaloes for milk production. India is the largest producer of milk in the world, and dairy farming plays a huge role in rural income.</p>
            
            <h4>2. Draught Animal Farming</h4>
            <p>In many villages, bulls and oxen are trained for ploughing, pulling carts, and other agricultural work. Even with modern machines, many farmers still depend on cattle power.</p>
            
            <h4>3. Mixed or Dual-Purpose Farming</h4>
            <p>Here, cattle are raised for both milk and draught power. This method is very common in India because it provides multiple benefits.</p>
            
            <h4>4. Commercial Cattle Farming</h4>
            <p>Large-scale farms focus on milk processing, meat export, or breeding improved cattle varieties. This method uses advanced technology, veterinary care, and scientific feeding.</p>
            
            <h3>Benefits of Cattle Farming</h3>
            <p>Cattle farming is valuable not just for farmers but for society as a whole. The benefits are wide-ranging:</p>
            
            <h4>1. Milk and Dairy Products</h4>
            <p>Cattle provide milk, which is turned into butter, ghee, curd, and cheese—an important source of nutrition.</p>
            
            <h4>2. Natural Fertilizer</h4>
            <p>Cow dung and urine are used as organic manure and bio-pesticides, reducing chemical dependency.</p>
            
            <h4>3. Energy Source</h4>
            <p>Biogas from dung is used for cooking and even electricity production in rural areas.</p>
            
            <h4>4. Employment</h4>
            <p>Millions of rural families earn livelihoods from cattle farming, directly or indirectly.</p>
            
            <h4>5. Cultural Value</h4>
            <p>In India, cows hold religious and cultural importance, adding emotional value to their practical role.</p>
            
            <h4>6. Sustainable Ecosystem</h4>
            <p>By recycling farm waste into manure, cattle play a role in balancing nature.</p>
            
            <h3>Purpose of Cattle Farming</h3>
            <p>The purpose of cattle farming goes beyond just profit. It includes:</p>
            <ul>
                <li>Ensuring food security through milk and meat.</li>
                <li>Providing draught power for agriculture in rural areas.</li>
                <li>Supporting sustainable agriculture by enriching soil fertility.</li>
                <li>Offering a steady income source for small and marginal farmers.</li>
            </ul>
            
            <h3>Role of Cattle in Agriculture in India</h3>
            <p>India has always been known as a land of cattle. Even today, cattle play a vital role in agriculture. Their role can be understood in different ways:</p>
            
            <h4>1. Ploughing and Field Work</h4>
            <p>Oxen are still used in villages for ploughing fields, sowing seeds, and carrying loads.</p>
            
            <h4>2. Soil Fertility</h4>
            <p>Cow dung is a rich source of organic matter. It improves soil texture and supports microbial life.</p>
            
            <h4>3. Sustainable Livelihoods</h4>
            <p>Cattle farming ensures steady milk supply, which provides daily income for farmers.</p>
            
            <h4>4. Agro-Energy</h4>
            <p>Biogas plants in villages reduce dependence on firewood and LPG.</p>
            
            <h4>5. Cultural and Spiritual Role</h4>
            <p>In Indian tradition, cattle are seen as sacred, symbolizing wealth and prosperity.</p>
            
            <h3>Cattle Farming and Sustainable Agriculture</h3>
            <p>Cattle farming is directly linked to sustainable agriculture. Unlike chemical-intensive farming, cattle-based systems recycle resources naturally. Dung and urine are turned into manure and bio-fertilizers, reducing chemical use. Cattle also make integrated farming possible—where crops, livestock, and energy production all work together.</p>
            
            <p>In many ways, cattle are the backbone of Indian farming. Without them, rural life would look very different.</p>
            
            <h3>Final Thoughts</h3>
            <p>Cattle farming is not just about milk or meat—it is about sustaining families, communities, and the entire agricultural system. From small farmers to large commercial farms, cattle continue to shape India's rural economy.</p>
            
            <p>As we move toward a greener future, cattle farming will remain a foundation of sustainable agriculture, balancing productivity with care for nature.</p>
            
            <blockquote>"Take care of cattle, and they will take care of your fields, your food, and your future."</blockquote>
            
            <h3>FAQs on Cattle Farming</h3>
            <h4>1. What is cattle farming in simple words?</h4>
            <p>It is the practice of raising cows, buffaloes, and oxen for milk, meat, draught power, and other products.</p>
            
            <h4>2. What are the types of cattle farming?</h4>
            <p>The main types are dairy farming, beef farming, draught animal farming, mixed farming, and commercial cattle farming.</p>
            
            <h4>3. Why is cattle farming important?</h4>
            <p>It provides milk, manure, employment, and supports agriculture in rural India.</p>''',
            'category': categories['Cattle Farming'],
            'tags': [tags['cattle'], tags['dairy'], tags['livestock'], tags['farming'], tags['sustainability']],
            'featured': True,
            'status': 'published',
            'image': 'blog-2.jpg'
        },
        {
            'title': 'Integrated Farming: Models, Pillars, and Role in Organic Agriculture',
            'summary': 'Discover the benefits of integrated farming. Learn the 7 pillars of an integrated intensive farming system, models in India, and the role of organic agriculture in sustainability.',
            'content': '''<h2>Introduction: What is Integrated Farming?</h2>
            <p>Integrated farming is a modern approach that combines crops, livestock, fisheries, poultry, and other enterprises on a single farm to maximize productivity and sustainability. Instead of focusing on just one activity, it creates a system where the waste from one becomes the input for another.</p>
            
            <p>In simple words, integrated farming is about creating a farm ecosystem where nothing goes to waste. For example, cow dung from dairy farming is used to make biogas or organic manure, while crop residues feed cattle and poultry.</p>
            
            <p>This method goes hand in hand with organic agriculture, because it reduces chemical dependence, restores soil fertility, and ensures long-term food security.</p>
            
            <blockquote>"An integrated farm is like a family—every member supports the other."</blockquote>
            
            <h3>What are the 7 Pillars of an Integrated Intensive Farming System?</h3>
            <p>The strength of integrated farming lies in its seven core pillars, each playing an important role in balancing productivity and sustainability.</p>
            
            <h4>1. Crop Production</h4>
            <ul>
                <li>Growing cereals, pulses, vegetables, and fruits.</li>
                <li>Crop diversity ensures year-round food and income.</li>
            </ul>
            
            <h4>2. Livestock Farming</h4>
            <ul>
                <li>Rearing cows, buffaloes, goats, or sheep for milk, meat, and manure.</li>
                <li>Livestock waste is recycled as compost or biogas.</li>
            </ul>
            
            <h4>3. Poultry Farming</h4>
            <ul>
                <li>Chickens, ducks, and turkeys add eggs and meat to the system.</li>
                <li>Poultry droppings enrich fish ponds or crop fields.</li>
            </ul>
            
            <h4>4. Fisheries (Aquaculture)</h4>
            <ul>
                <li>Fish farming in ponds or tanks integrates with poultry and livestock.</li>
                <li>Droppings act as pond nutrients, reducing external feed costs.</li>
            </ul>
            
            <h4>5. Agro-Forestry</h4>
            <ul>
                <li>Planting trees on farmland provides fodder, timber, and shade.</li>
                <li>It also improves biodiversity and soil health.</li>
            </ul>
            
            <h4>6. Biogas and Renewable Energy</h4>
            <ul>
                <li>Dung and crop residues are converted into energy.</li>
                <li>Farmers save on fuel and fertilizer costs.</li>
            </ul>
            
            <h4>7. Value Addition and Marketing</h4>
            <ul>
                <li>Processing products like milk into ghee, or fruits into jams.</li>
                <li>Direct selling through farmers' markets increases profit margins.</li>
            </ul>
            
            <p>Together, these seven pillars make the integrated farming system intensive, profitable, and sustainable.</p>
            
            <h3>Integrated Farming System Model</h3>
            <p>The integrated farming system (IFS) model is designed to link different enterprises for better resource use. A typical model includes:</p>
            <ul>
                <li>Crops (rice, wheat, vegetables, fruits)</li>
                <li>Dairy unit (cows or buffaloes)</li>
                <li>Poultry unit (chickens, ducks)</li>
                <li>Fish pond (carp, catla, rohu)</li>
                <li>Biogas plant (using cow dung)</li>
                <li>Agro-forestry (timber, fodder, medicinal plants)</li>
            </ul>
            
            <p>In this cycle:</p>
            <ul>
                <li>Crop residues feed livestock.</li>
                <li>Manure and droppings fertilize fields or ponds.</li>
                <li>Biogas plant provides clean energy.</li>
                <li>Trees add extra income and ecological balance.</li>
            </ul>
            
            <p>This circular system reduces waste, improves income security, and makes farming resilient to climate change.</p>
            
            <h3>Integrated Farming in India</h3>
            <p>India has been practicing integrated farming for centuries, even before the term was coined. Small farmers, in particular, benefit greatly from IFS because it:</p>
            
            <h4>1. Reduces Risk</h4>
            <ul>
                <li>Even if one crop fails, income from dairy or poultry sustains the family.</li>
            </ul>
            
            <h4>2. Increases Income</h4>
            <ul>
                <li>Multiple enterprises mean continuous cash flow instead of seasonal earnings.</li>
            </ul>
            
            <h4>3. Promotes Local Employment</h4>
            <ul>
                <li>Family members stay engaged year-round.</li>
            </ul>
            
            <h4>4. Adapts to Climate</h4>
            <ul>
                <li>Crop diversity and livestock integration make farms more climate-resilient.</li>
            </ul>
            
            <p>Across India, integrated farming is gaining attention, especially in states like Kerala, Tamil Nadu, and Andhra Pradesh. Many government schemes also promote IFS for small and marginal farmers.</p>
            
            <h3>What is the Role of Organic Agriculture in Integrated Farming?</h3>
            <p>The success of integrated farming depends heavily on organic agriculture. Without relying on chemicals, organic inputs from cattle, poultry, and crops keep the system natural and productive.</p>
            
            <ul>
                <li><strong>Soil Fertility:</strong> Dung, compost, and green manure enrich soil naturally.</li>
                <li><strong>Pest Control:</strong> Poultry and ducks help control pests in fields and ponds.</li>
                <li><strong>Eco-Balance:</strong> Trees, animals, and crops create a balanced environment.</li>
                <li><strong>Sustainable Yields:</strong> Organic methods ensure long-term productivity.</li>
            </ul>
            
            <p>In India, where small farms dominate, combining integrated farming with organic agriculture is the way forward. It ensures food safety, better income, and protection of natural resources.</p>
            
            <h3>Advantages of Integrated Farming</h3>
            <ol>
                <li><strong>Waste Utilization</strong> – Nothing goes unused; waste is recycled.</li>
                <li><strong>Diversified Income</strong> – Reduces dependency on one source.</li>
                <li><strong>Low Cost of Production</strong> – Natural inputs reduce expenses.</li>
                <li><strong>Eco-Friendly</strong> – Supports biodiversity and reduces pollution.</li>
                <li><strong>Nutritional Security</strong> – Provides milk, eggs, fish, fruits, and vegetables from one farm.</li>
                <li><strong>Climate Resilience</strong> – Protects farmers from extreme weather risks.</li>
            </ol>
            
            <h3>Final Thoughts</h3>
            <p>Integrated farming is not just a technique—it's a vision of sustainable rural development. By combining crops, livestock, fisheries, and forestry, it creates a system that is eco-friendly, profitable, and self-sufficient.</p>
            
            <p>And at the heart of it lies organic agriculture, which turns farming into a natural cycle where soil, plants, and animals thrive together.</p>
            
            <blockquote>"An integrated farm is nature's way of showing us that everything is connected."</blockquote>
            
            <p>If farmers adopt integrated farming widely, India can achieve food security, rural prosperity, and environmental protection together.</p>
            
            <h3>FAQs</h3>
            <h4>1. What is integrated farming in simple words?</h4>
            <p>It is a farming method where crops, livestock, fish, and trees are grown together for maximum benefit.</p>
            
            <h4>2. What are the 7 pillars of integrated farming?</h4>
            <p>Crops, livestock, poultry, fisheries, agro-forestry, biogas/energy, and value addition.</p>
            
            <h4>3. What is the link between organic agriculture and integrated farming?</h4>
            <p>Organic agriculture provides natural manure, pest control, and soil fertility that make integrated farming sustainable.</p>''',
            'category': categories['Integrated Farming'],
            'tags': [tags['integrated-farming'], tags['sustainability'], tags['farming'], tags['biodiversity'], tags['organic']],
            'featured': True,
            'status': 'published',
            'image': 'blog-3.jpg'
        },
        {
            'title': 'Vermicompost: Uses, Process, and Market in India',
            'summary': 'Discover the benefits of vermicompost. Learn vermicompost uses, the step-by-step process, and how the vermicompost market is growing in India for sustainable farming.',
            'content': '''<h2>Introduction: What is Vermicompost?</h2>
            <p>Vermicompost is a natural organic fertilizer made by using earthworms to convert biodegradable waste into nutrient-rich compost. It is often called "black gold" because it enriches soil with essential nutrients and beneficial microbes. Unlike chemical fertilizers, vermicompost improves soil structure, boosts crop yield, and protects the environment.</p>
            
            <p>One of the most powerful aspects of this method is vermicompost uses in farming and gardening. It is not only a fertilizer but also a sustainable solution to waste management. Farmers and gardeners across India are turning to vermicompost because it supports healthy crops while reducing dependency on chemicals.</p>
            
            <blockquote>"Earthworms are silent workers, but their work builds the foundation of healthy soil."</blockquote>
            
            <h3>Vermicompost Uses</h3>
            <p>The applications of vermicompost are diverse and highly beneficial. Here are the major vermicompost uses:</p>
            
            <h4>1. Soil Enrichment</h4>
            <p>Improves soil fertility by adding organic matter and essential nutrients.</p>
            
            <h4>2. Plant Growth Enhancement</h4>
            <p>Contains hormones and enzymes that promote root development and better yield.</p>
            
            <h4>3. Waste Recycling</h4>
            <p>Converts kitchen waste, farm residues, and animal manure into valuable compost.</p>
            
            <h4>4. Water Retention</h4>
            <p>Increases the soil's capacity to hold water, reducing irrigation needs.</p>
            
            <h4>5. Pest and Disease Resistance</h4>
            <p>Strengthens plants against common diseases and reduces chemical pesticide use.</p>
            
            <h4>6. Universal Application</h4>
            <p>Safe for all types of crops, from cereals to vegetables, fruits, flowers, and medicinal plants.</p>
            
            <h3>Vermicompost Process</h3>
            <p>The process of making vermicompost is simple, cost-effective, and eco-friendly. Here's how it works:</p>
            
            <h4>1. Selection of Site and Container</h4>
            <p>Choose a shaded area to avoid direct sunlight. Use a cement tank, wooden box, or plastic bin as the container.</p>
            
            <h4>2. Bedding Preparation</h4>
            <p>Place materials like dry leaves, husk, shredded paper, or coconut coir at the bottom. This creates a soft base for the worms.</p>
            
            <h4>3. Addition of Organic Waste</h4>
            <p>Add layers of kitchen waste, cow dung, and crop residues. Avoid meat, oily food, and plastics.</p>
            
            <h4>4. Introduction of Earthworms</h4>
            <p>Use species like Eisenia fetida (red wigglers) or Eudrilus eugeniae. They are efficient at decomposing organic matter.</p>
            
            <h4>5. Moisture and Temperature Management</h4>
            <p>Keep the system damp but not waterlogged. Ideal moisture is around 60–70%, with temperatures between 20–30°C.</p>
            
            <h4>6. Decomposition Period</h4>
            <p>Earthworms eat the waste, digest it, and release fine, granular compost known as worm castings.</p>
            
            <h4>7. Harvesting Vermicompost</h4>
            <p>Within 45–60 days, the compost is ready. It appears dark, crumbly, and odorless. Separate the worms and use the compost for farming.</p>
            
            <p>This cycle makes vermicomposting an ideal waste-to-wealth model for both homes and farms.</p>
            
            <h3>Vermicompost Market in India</h3>
            <p>India is witnessing rapid growth in the vermicompost market, driven by rising awareness of organic farming and sustainable practices.</p>
            
            <h4>1. Increasing Demand</h4>
            <ul>
                <li>Farmers are shifting from chemical fertilizers to organic inputs.</li>
                <li>Consumers prefer chemical-free food, boosting demand for organic crops.</li>
                <li>Vermicompost is now sold in retail stores, online platforms, and local markets.</li>
            </ul>
            
            <h4>2. Government Support</h4>
            <p>Schemes promoting organic farming, like Paramparagat Krishi Vikas Yojana (PKVY), encourage farmers to adopt vermicomposting.</p>
            
            <h4>3. Business Opportunities</h4>
            <p>Small-scale entrepreneurs and rural youth are setting up vermicompost units. Low investment and high demand make it a profitable venture.</p>
            
            <h4>4. Export Potential</h4>
            <p>With global demand for organic produce increasing, Indian vermicompost producers have opportunities in international markets.</p>
            
            <h4>5. Market Challenges</h4>
            <ul>
                <li>Lack of awareness in remote areas.</li>
                <li>Quality control issues.</li>
                <li>Need for better packaging and branding.</li>
            </ul>
            
            <p>Despite challenges, the vermicompost market in India is expected to grow steadily, providing income and employment in rural communities.</p>
            
            <h3>Advantages of Vermicompost</h3>
            <ol>
                <li>Improves soil structure and aeration.</li>
                <li>Provides balanced nutrients for crops.</li>
                <li>Reduces chemical fertilizer dependency.</li>
                <li>Converts waste into useful fertilizer.</li>
                <li>Environmentally safe and pollution-free.</li>
                <li>Supports sustainable farming systems.</li>
            </ol>
            
            <h3>Final Thoughts</h3>
            <p>Vermicompost is not just a fertilizer—it is a bridge between waste management, soil health, and sustainable farming. With its ability to recycle organic waste and provide natural nutrients, it has become essential for farmers and gardeners alike.</p>
            
            <p>The future of farming in India depends on eco-friendly solutions, and vermicompost is at the heart of it. When combined with organic and integrated farming practices, it creates a cycle of productivity that benefits farmers, consumers, and the environment.</p>
            
            <p>At its core, vermicomposting strengthens organic agriculture, ensuring safe food, healthy soil, and a cleaner planet. And in every farm or garden where earthworms work, they remind us of the value of nature's smallest workers.</p>
            
            <blockquote>"Healthy soil grows healthy food, and healthy food builds healthy lives."</blockquote>
            
            <p>So, whether you are a farmer or a gardener, embracing vermicompost uses is a step toward a sustainable and profitable future.</p>
            
            <h3>FAQs</h3>
            <h4>1. What is vermicompost in simple words?</h4>
            <p>It is an organic fertilizer made by earthworms processing organic waste into compost.</p>
            
            <h4>2. What are vermicompost uses?</h4>
            <p>It enriches soil, boosts crop growth, recycles waste, improves water retention, and supports pest resistance.</p>
            
            <h4>3. How long does it take to make vermicompost?</h4>
            <p>Usually, 45–60 days depending on waste, moisture, and worm activity.</p>
            
            <h4>4. Is vermicomposting profitable in India?</h4>
            <p>Yes, it is in high demand, low cost to produce, and supported by government schemes.</p>''',
            'category': categories['Composting'],
            'tags': [tags['vermicompost'], tags['composting'], tags['organic'], tags['sustainability'], tags['soil-health']],
            'featured': False,
            'status': 'published',
            'image': 'blog-4.jpg'
        },
        {
            'title': 'Pragathi Natural Farm: Cultivating a Self-Sustaining Organic Ecosystem',
            'summary': 'Pragathi Natural Farm in Pollachi practices organic farming with biodiversity and integrated farming for a self-sustainable future.',
            'content': '''<h2>Pragathi Natural Farm: Cultivating a Self-Sustaining Organic Ecosystem</h2>
            <p>Nestled amidst the serene landscapes of Jakkarpalaym, Pollachi, Pragathi Natural Farm is not just a farm—it's a thriving, self-sustainable, biodiverse organic ecosystem. Here, every element—soil, plants, livestock, and humans—works in unity, forming a living cycle of growth and regeneration.</p>
            
            <h3>A Model of Integrated Sustainability</h3>
            <p>Pragathi Natural Farm embodies the essence of integrated, sustainable agriculture. This approach transforms farming into an ecosystem where:</p>
            <ul>
                <li>Crop cultivation, livestock rearing, and composting are seamlessly integrated.</li>
                <li>Waste becomes a resource—farm residues feed animals, and their waste becomes compost.</li>
                <li>Biodiversity is prioritized—a healthy diversity of plants and animals strengthens the system's resilience.</li>
            </ul>
            
            <p>Their model demonstrates how small-scale farms can thrive economically while staying ecologically balanced.</p>
            
            <h3>Rooted in Biodiversity</h3>
            <p>At Pragathi, biodiversity isn't merely a principle—it's a living reality. A variety of crops, indigenous plants, and beneficial organisms coexist, creating a robust ecological network. This rich biodiversity:</p>
            <ul>
                <li>Enhances soil fertility naturally.</li>
                <li>Encourages native pollinators and pest-controlling species.</li>
                <li>Makes the farm resilient against climate fluctuations.</li>
            </ul>
            
            <h3>Organic Practices at the Core</h3>
            <p>Pragathi Natural Farm operates on organic principles—zero synthetic chemicals, minimal external inputs, and maximum reliance on natural processes. By doing so, the farm:</p>
            <ul>
                <li>Nurtures healthy, breathable soil.</li>
                <li>Produces chemical-free food with integrity.</li>
                <li>Upholds environmentally safe and sustainable farming.</li>
            </ul>
            
            <p>These practices also align with growing consumer demand for clean, trustworthy agricultural produce.</p>
            
            <h3>Sustainability in Every Cycle</h3>
            <p>What sets Pragathi apart is how each component of the farm supports others:</p>
            <ul>
                <li>Crop by-products feed compost piles or animals.</li>
                <li>Animal waste turns into nutritious compost or organic fertilizer.</li>
                <li>Compost nourishes the soil, completing the cycle of renewal.</li>
            </ul>
            
            <p>This closed-loop system cuts waste, lowers costs, and nurtures long-term productivity.</p>
            
            <h3>Community and Innovation</h3>
            <p>Beyond farming, Pragathi Natural Farm serves as a beacon of inspiration for local communities. Such integrated, ecological farming methods:</p>
            <ul>
                <li>Offer trainings and models for sustainable rural livelihoods.</li>
                <li>Empower farmers to shift toward low-cost, high-value systems.</li>
                <li>Encourage knowledge-sharing and local adaptation.</li>
            </ul>
            
            <p>In doing so, Pragathi becomes more than a farm—it becomes a hub for regenerative agriculture in the region.</p>
            
            <h3>Final Thoughts</h3>
            <p>Pragathi Natural Farm showcases how organic, biodiverse, and self-sustainable farming systems are not just possible—they are scalable, profitable, and regenerative. Situated in Pollachi, this farm proves that with thoughtful design and integrated cycles, agriculture can heal the soil, sustain livelihoods, and uplift communities.</p>
            
            <p>As we look toward the future of farming, Pragathi Natural Farm stands as a testament to what is possible when we work with nature rather than against it. Their success demonstrates that sustainable agriculture is not just an ideal—it's a practical, profitable, and necessary path forward.</p>
            
            <blockquote>"The future of farming lies in harmony with nature, where every element supports the other in a cycle of continuous growth and renewal."</blockquote>
            
            <p>Visit Pragathi Natural Farm in Jakkarpalaym, Pollachi, to witness firsthand how sustainable agriculture can transform not just land, but entire communities and ecosystems.</p>''',
            'category': categories['Farm Stories'],
            'tags': [tags['pragathi-farm'], tags['pollachi'], tags['biodiversity'], tags['self-sustainable'], tags['organic'], tags['integrated-farming']],
            'featured': True,
            'status': 'published',
            'image': 'blog-5.jpg'
        }
    ]
    
    # Create blogs with images
    for i, blog_data in enumerate(blogs_data):
        # Set published date (recent dates)
        days_ago = i * 2  # Spread over 10 days
        published_date = timezone.now() - timedelta(days=days_ago)
        
        blog, created = Blog.objects.get_or_create(
            title=blog_data['title'],
            defaults={
                'summary': blog_data['summary'],
                'content': blog_data['content'],
                'category': blog_data['category'],
                'author': admin_user,
                'status': blog_data['status'],
                'featured': blog_data['featured'],
                'published_date': published_date,
                'meta_title': blog_data['title'],
                'meta_description': blog_data['summary'][:300]
            }
        )
        
        if created:
            blog.tags.set(blog_data['tags'])
            
            # Add image if specified
            if 'image' in blog_data and blog_data['image']:
                image_path = f'/home/sasikalavijayakumar/pragathi_server/PRAGATHI-UI/public/assets/{blog_data["image"]}'
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        django_file = File(f)
                        blog.thumbnail.save(
                            blog_data['image'],
                            ContentFile(f.read()),
                            save=True
                        )
                    print(f"📸 Added image {blog_data['image']} to blog: {blog.title}")
                else:
                    print(f"⚠️ Image not found: {image_path}")
            
            print(f"✅ Created blog: {blog.title}")
        else:
            print(f"ℹ️ Blog already exists: {blog.title}")
    
    print(f"\n🎉 Comprehensive blog deployment completed!")
    print(f"📊 Summary:")
    print(f"   • Categories: {len(categories)}")
    print(f"   • Tags: {len(tags)}")
    print(f"   • Blogs created: {len(blogs_data)}")
    print(f"   • Images processed: {len([b for b in blogs_data if 'image' in b])}")

if __name__ == '__main__':
    try:
        deploy_comprehensive_blogs()
    except Exception as e:
        print(f"❌ Error deploying comprehensive blogs: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
