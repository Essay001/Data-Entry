import flet as ft
import datetime

# --- Mock Data ---
INITIAL_REVIEWS = [
    {
        'id': 1,
        'user_name': "Party Marty",
        'user_avatar': "https://loremflickr.com/100/100/man,smile", 
        'restaurant': "St. Stan's Social Hall", 
        'location': "Milwaukee, WI",
        'rating': 5, 
        'crispiness': 'Perfect', 
        'tartar': 'Tangy', 
        'notes': 'The polka band was on fire! Best cod in the county.',
        'date': 'Oct 12',
        'image': 'https://loremflickr.com/320/240/fish,food',
        'tagged': ['Big Tony', 'Cousin Sal'],
        'toasts': 12,
        'comments': 3
    },
    {
        'id': 2, 
        'user_name': "Party Marty",
        'user_avatar': "https://loremflickr.com/100/100/man,smile",
        'restaurant': "Joe's Lakeside Pub", 
        'location': "Madison, WI",
        'rating': 3, 
        'crispiness': 'Soggy', 
        'tartar': 'Bland', 
        'notes': 'Good beer, but the fish needs work. Cole slaw was watery.',
        'date': 'Oct 19',
        'image': None,
        'tagged': [],
        'toasts': 2,
        'comments': 0
    },
    {
        'id': 3, 
        'user_name': "Cousin Sal",
        'user_avatar': "https://loremflickr.com/100/100/boy,smile",
        'restaurant': "The Walleye Wagon", 
        'location': "Green Bay, WI",
        'rating': 4, 
        'crispiness': 'Crunchy', 
        'tartar': 'Good', 
        'notes': 'Solid choice for a Friday night.',
        'date': 'Oct 20',
        'image': None,
        'tagged': ['Party Marty'],
        'toasts': 5,
        'comments': 1
    },
]

NEARBY_SPOTS = [
    {'name': "The Walleye Wagon", 'dist': '0.8 mi', 'rating': 4.8},
    {'name': "Betty's Breading Barn", 'dist': '1.2 mi', 'rating': 4.2},
    {'name': "VFW Post #209", 'dist': '2.5 mi', 'rating': 5.0},
    {'name': "Captain Mike's", 'dist': '3.1 mi', 'rating': 3.5},
]

BADGES = [
    {'name': 'Cod Commander', 'icon': '👑', 'desc': 'Rated 10 places'},
    {'name': 'Tartar Titan', 'icon': '🥒', 'desc': 'Found the perfect sauce'},
    {'name': 'Friday Fanatic', 'icon': '📅', 'desc': '4 weeks in a row'},
    {'name': 'Polka Pro', 'icon': '🪗', 'desc': 'Danced at dinner'},
]

FRIENDS = ['Big Tony', 'Cousin Sal', 'Fishing Fred', 'Aunt Linda']

def main(page: ft.Page):
    print("Starting Party Marty's App...") # Debug message for console
    
    # --- Page Configuration ---
    page.title = "Party Marty's Fry Finder"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window_width = 390
    page.window_height = 844
    page.bgcolor = "#f5f5f5" # Light grey background typical of social apps

    # --- State ---
    reviews = INITIAL_REVIEWS.copy()
    
    # --- Helper Components ---
    def get_fish_rating(rating):
        # Returns a row of fish icons based on rating
        fish_row = ft.Row(spacing=2)
        for i in range(5):
            if i < rating:
                fish_row.controls.append(ft.Text("🐟", size=14))
            else:
                fish_row.controls.append(ft.Text("🦴", size=14, color="grey"))
        return fish_row

    class ReviewCard(ft.Card):
        def __init__(self, review, on_delete):
            super().__init__()
            self.review = review
            self.elevation = 0
            self.margin = ft.margin.only(bottom=10)
            self.color = "white"
            self.shape = ft.RoundedRectangleBorder(radius=0) # Squared off for feed look
            
            # Fish Rating Row
            fish_scale = get_fish_rating(review['rating'])

            # Image logic
            img_container = ft.Container()
            if review['image']:
                img_container = ft.Container(
                    content=ft.Image(
                        src=review['image'],
                        fit=ft.ImageFit.COVER,
                        width=float("inf"),
                        height=200,
                    ),
                    border_radius=8,
                    margin=ft.margin.only(top=10, bottom=10),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE
                )

            # Avatar
            avatar = ft.Container(
                content=ft.Image(src=review['user_avatar'], fit=ft.ImageFit.COVER),
                width=40, height=40, border_radius=20, clip_behavior=ft.ClipBehavior.HARD_EDGE
            )

            # Header Text (Untappd Style)
            # "User is eating Fish at Location"
            header_text = ft.Column([
                ft.Row([
                    ft.Text(review['user_name'], weight="bold", color="blue", size=14),
                    ft.Text("is eating fish at", size=14),
                ], spacing=4, wrap=True),
                ft.Text(review['restaurant'], weight="bold", color="amber900", size=14),
                ft.Text(review.get('location', 'Unknown'), size=12, color="grey"),
            ], spacing=2)

            self.content = ft.Container(
                padding=15,
                content=ft.Column([
                    # Top Row: Avatar + Info + Time
                    ft.Row([
                        avatar,
                        ft.Container(content=header_text, expand=True),
                        ft.Icon("more_horiz", color="grey") # Menu icon
                    ], vertical_alignment="start"),

                    # The Check-in Content
                    ft.Container(
                        padding=ft.padding.only(left=50), # Indent to align with text, not avatar
                        content=ft.Column([
                            ft.Text(f"\"{review['notes']}\"", size=14, color="black87"),
                            
                            # Attributes
                            ft.Row([
                                ft.Container(
                                    padding=5, bgcolor="orange50", border_radius=5,
                                    content=ft.Row([ft.Text("Crispiness:", size=10, color="orange900"), ft.Text(review['crispiness'], size=10, weight="bold", color="orange900")])
                                ),
                                fish_scale
                            ], alignment="spaceBetween"),

                            img_container,

                            # Action Bar (Toast/Comment)
                            ft.Divider(color="grey200"),
                            ft.Row([
                                ft.Row([
                                    ft.Icon("local_bar", size=16, color="amber"), # "Toast" icon
                                    ft.Text(f"Toast ({review.get('toasts', 0)})", size=12, weight="bold", color="grey700")
                                ], spacing=5),
                                ft.Row([
                                    ft.Icon("chat_bubble_outline", size=16, color="grey"),
                                    ft.Text(f"Comment ({review.get('comments', 0)})", size=12, weight="bold", color="grey700")
                                ], spacing=5),
                            ], spacing=20)
                        ])
                    )
                ])
            )

    # --- Views ---
    
    def build_home_view():
        # Untappd Header is usually simple
        header = ft.Container(
            padding=ft.padding.only(left=15, right=15, top=50, bottom=15),
            bgcolor="amber700", # The "Beer/Fry" Gold Color
            content=ft.Row([
                ft.Text("Nearby Activity", color="white", size=18, weight="bold"),
                ft.Icon("notifications", color="white")
            ], alignment="spaceBetween")
        )

        review_list = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)
        
        def refresh_list():
            review_list.controls.clear()
            for r in reviews:
                review_list.controls.append(ReviewCard(r, delete_review))
            # Add some padding at bottom so FAB doesn't cover last item
            review_list.controls.append(ft.Container(height=80)) 
            page.update()

        def delete_review(id):
            reviews[:] = [r for r in reviews if r['id'] != id]
            refresh_list()

        refresh_list()

        # --- Check-In Dialog Logic ---
        def show_add_dialog(e):
            # Form Fields
            name_field = ft.TextField(label="Where are you eating?", icon="search", border_radius=30)
            
            # Location Field with GPS Button
            loc_field = ft.TextField(label="Location", value="Current Location", expand=True, text_size=12)
                
            # Fish Rating Slider
            rating_label = ft.Text("Rating: 3 Fish 🐟🐟🐟", weight="bold")
            def slider_change(e):
                val = int(e.control.value)
                rating_label.value = f"Rating: {val} Fish " + ("🐟" * val)
                rating_label.update()

            rating_slider = ft.Slider(
                min=1, max=5, divisions=4, value=3, 
                label="{value}", on_change=slider_change, active_color="amber"
            )
            
            crisp_field = ft.Dropdown(
                label="Crispiness",
                options=[ft.dropdown.Option("Soggy"), ft.dropdown.Option("Decent"), ft.dropdown.Option("Crunchy"), ft.dropdown.Option("Perfect")],
            )
            note_field = ft.TextField(label="What did you think?", multiline=True, min_lines=3)
            
            # File Picker
            uploaded_file_text = ft.Text("Add Photo", size=12, weight="bold", color="blue")
            def pick_files_result(e: ft.FilePickerResultEvent):
                if e.files:
                    uploaded_file_text.value = "Photo Attached!"
                    uploaded_file_text.color = "green"
                    uploaded_file_text.update()

            file_picker = ft.FilePicker(on_result=pick_files_result)
            page.overlay.append(file_picker)

            def save_review(e):
                if not name_field.value: return
                
                reviews.insert(0, {
                    'id': int(datetime.datetime.now().timestamp()),
                    'user_name': "Party Marty", # Current user
                    'user_avatar': "https://loremflickr.com/100/100/man,smile",
                    'restaurant': name_field.value,
                    'location': "Milwaukee, WI", # Mock GPS
                    'rating': int(rating_slider.value),
                    'crispiness': crisp_field.value if crisp_field.value else "Decent",
                    'tartar': "Good",
                    'notes': note_field.value,
                    'date': "Just now",
                    'image': "https://loremflickr.com/320/240/fish,chips" if uploaded_file_text.value == "Photo Attached!" else None,
                    'tagged': [],
                    'toasts': 0,
                    'comments': 0
                })
                refresh_list()
                page.dialog.open = False
                page.update()

            page.dialog = ft.AlertDialog(
                title=ft.Text("Check-In", weight="bold"),
                content=ft.Column([
                    name_field,
                    ft.Row([ft.Icon("location_on", size=16), loc_field]),
                    ft.Divider(),
                    note_field,
                    rating_label, 
                    rating_slider,
                    ft.Row([
                        ft.IconButton("camera_alt", on_click=lambda _: file_picker.pick_files()),
                        uploaded_file_text
                    ]), 
                    crisp_field, 
                ], height=400, scroll=ft.ScrollMode.AUTO),
                actions=[
                    ft.ElevatedButton("Confirm Check-In", bgcolor="amber700", color="white", on_click=save_review)
                ]
            )
            page.dialog.open = True
            page.update()

        return ft.Stack([
            ft.Column([
                header,
                ft.Container(
                    content=review_list,
                    expand=True
                )
            ], expand=True),
            
            # The "Untappd" Style Check-in Button
            ft.Container(
                alignment=ft.alignment.bottom_center,
                padding=20,
                content=ft.ElevatedButton(
                    text="CHECK-IN",
                    icon="add",
                    bgcolor="amber700",
                    color="white",
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=30)),
                    on_click=show_add_dialog
                )
            )
        ])

    def build_map_view():
        spots_list = ft.Column(spacing=2)
        
        for spot in NEARBY_SPOTS:
            spots_list.controls.append(
                ft.Container(
                    padding=15, bgcolor="white", 
                    margin=ft.margin.only(bottom=1),
                    content=ft.Row([
                        ft.Column([
                            ft.Text(spot['name'], weight="bold", size=16),
                            ft.Text("Fried Fish • American", size=12, color="grey"),
                            ft.Text(f"{spot['dist']} away", size=12, color="amber700")
                        ]),
                        ft.Container(
                            padding=10, bgcolor="amber100", border_radius=10,
                            content=ft.Column([
                                ft.Text(str(spot['rating']), weight="bold", color="amber900", size=16),
                            ], alignment="center")
                        )
                    ], alignment="spaceBetween")
                )
            )

        return ft.Column([
            ft.Container(
                padding=ft.padding.only(top=50, left=15, right=15, bottom=15), 
                bgcolor="amber700",
                content=ft.Text("Verified Venues", color="white", size=18, weight="bold")
            ),
            ft.Container(
                content=ft.Image(
                    src="https://loremflickr.com/400/200/map,city", 
                    fit=ft.ImageFit.COVER,
                    width=float("inf"),
                    height=200,
                ),
                height=200, width=float("inf")
            ),
            ft.Container(content=spots_list, expand=True)
        ], expand=True)

    def build_profile_view():
        # Stats Row (Total, Unique, Badges)
        stats_row = ft.Row([
            ft.Column([ft.Text("124", weight="bold", size=18), ft.Text("TOTAL", size=10, color="grey")], horizontal_alignment="center"),
            ft.Column([ft.Text("48", weight="bold", size=18), ft.Text("UNIQUE", size=10, color="grey")], horizontal_alignment="center"),
            ft.Column([ft.Text("12", weight="bold", size=18), ft.Text("BADGES", size=10, color="grey")], horizontal_alignment="center"),
            ft.Column([ft.Text("85", weight="bold", size=18), ft.Text("FRIENDS", size=10, color="grey")], horizontal_alignment="center"),
        ], alignment="spaceEvenly", spacing=20)

        badge_row = ft.Row(wrap=True, spacing=15, alignment="center")
        for b in BADGES:
            badge_row.controls.append(
                ft.Column([
                    ft.Container(
                        padding=15, bgcolor="amber100", border_radius=30,
                        border=ft.border.all(2, "amber700"),
                        content=ft.Text(b['icon'], size=30)
                    ),
                    ft.Text(b['name'], size=10, weight="bold", text_align="center", width=70)
                ], horizontal_alignment="center")
            )

        return ft.ListView([
            # Profile Header with Banner style
            ft.Container(
                height=220,
                content=ft.Stack([
                    ft.Container(bgcolor="amber700", height=120), # Color banner
                    ft.Container(
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=60),
                        content=ft.Column([
                            ft.Container(
                                width=100, height=100, border_radius=50, 
                                border=ft.border.all(4, "white"),
                                content=ft.Image(src="https://loremflickr.com/100/100/man,smile", fit=ft.ImageFit.COVER),
                                clip_behavior=ft.ClipBehavior.HARD_EDGE
                            ),
                            ft.Text("Party Marty", size=22, weight="bold"),
                            ft.Text("Milwaukee, WI", color="grey", size=12),
                        ], horizontal_alignment="center")
                    )
                ])
            ),
            
            ft.Container(height=20),
            stats_row,
            ft.Divider(height=40),
            
            ft.Container(padding=20, content=ft.Text("Recent Badges", weight="bold", size=16)),
            ft.Container(padding=10, content=badge_row),
            
            ft.Divider(),
            ft.Container(padding=20, content=ft.Text("Recent Activity", weight="bold", size=16)),
             # We can reuse the feed here in a real app
             ft.Container(padding=20, content=ft.Text("Displaying recent check-ins...", color="grey"))

        ], padding=0)

    # --- Navigation Logic ---
    body_container = ft.Container(expand=True)

    def navigate_to(index):
        body_container.content = [
            build_home_view(),
            build_map_view(),
            build_profile_view()
        ][index]
        page.update()

    page.add(
        body_container,
        ft.NavigationBar(
            bgcolor="white",
            indicator_color="amber100",
            destinations=[
                ft.NavigationBarDestination(icon="dynamic_feed", label="Feed"),
                ft.NavigationBarDestination(icon="map", label="Map"),
                ft.NavigationBarDestination(icon="person", label="Profile"),
            ],
            on_change=lambda e: navigate_to(e.control.selected_index)
        )
    )
    
    navigate_to(0)

ft.app(target=main)
