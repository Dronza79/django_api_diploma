var mix = {
    methods: {
        getProfile() {
            this.getData(`/api/profile/`).then(data => {
                this.fullName = data.fullName
                this.avatar = data.avatar
                this.phone = data.phone
                this.email = data.email
            }).catch(() => {
                console.warn('Ошибка при получении профиля')
            })
        },
        changeProfile () {
            if(!this.fullName.trim().length || !this.phone.trim().length || !this.email.trim().length) {
                alert('В форме присутствуют незаполненные поля')
                return
            }

            this.postData('/api/profile/', {
                fullName: this.fullName,
                avatar: this.avatar,
                phone: this.phone,
                email: this.email
            }).then(data => {
               alert('Успешно сохранено')
            }).catch(() => {
                console.warn('Ошибка при обновлении профиля')
            })
        },
        changePassword () {
            if (
                !this.passwordCurrent.trim().length ||
                !this.password.trim().length ||
                !this.passwordReply.trim().length ||
                this.password !== this.passwordReply
            ) {
                alert('В форме присутствуют незаполненные поля или пароли не совпадают')
                return
            }
            this.postData('/api/profile/password').then(data => {
               alert('Успешно сохранено')
                this.passwordCurrent = ''
                this.password = ''
                this.passwordReply = ''
            }).catch(() => {
                console.warn('Ошибка при сохранении пароля')
            })
        },
        setAvatar (event) {
            const target = event.target
            const file = target.files?.[0] ?? null
            if (!file) return

            this.postData('/api/profile/avatar', file, {
                headers: {
                  'Content-Type': file.type,
                  'X-CSRFToken': this.getCookie('csrftoken')
                },
            }).then((data) => {
                this.avatar = data.url
            }).catch(() => {
                 console.warn('Ошибка при обновлении изображения')
            })
        },
    },
    created() {
        this.getProfile();
    },
    data() {
        return {
            fullName: null,
            phone: null,
            email: null,
            avatar: null,
            password: '',
            passwordCurrent: '',
            passwordReply: ''
        }
    },
}