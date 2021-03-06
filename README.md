# Modelplex

## 基本介绍

### 项目背景与小组成员

本项目是2022年春季北京大学软件工程实验班的课程项目，参与项目的小组成员为：刘昊文，尹轶，于程，张荟萱，张天耀（按音序排列，排名不分先后）

本网站的目的是提供一个开放的模型测试平台用于服务深度学习领域研究人员对于模型测试和复现的需要——传统的模型测试和复现方法操作相对复杂，对于每个单独的模型都需要研究人员自行搜寻源代码并按照说明配置环境与部署代码，有时还需要重写代码或对模型进行重新训练，而本网站旨在让模型提供者提供一份训练好的模型文件，而需要对模型进行测试和复现的研究人员只需按要求提供数据集即可，这样大幅度减轻了对模型测试和复现的研究者的工作量。而对于模型提供者而言也可以使模型通过更广泛的测试，有利于为模型性能的进一步提升和优化确定目标。

### 项目基本实现情况

本项目的网站端基于Django框架搭建，后续代码会在github上开源。服务器端使用了阿里云服务器，对模型的运行则是在服务器本地运行，服务器端配置了合适版本的pytorch与tensorflow，可以支持绝大多数主流模型的测试与运行。

本项目的网页渲染使用uoj的开源css代码与一些javascript代码，在这一基础上进行了二次开发得到，为了美观首页上添加了一张图片（图源网络，写公告的人不知道这是什么图，侵删）

## 网站使用

### 登录与注册

在未登录状态下，您可以在右上角看到登录和注册选项，点击登录进入*登录页面*，点击注册进入*注册页面*，我们目前并不需要验证码，用户输入合适的用户名和密码即可成功登录注册。

用户名必须为**英文字母数字下划线和横杠**，密码必须为**英文字母和数字**。 用户名和密码长度限制**20**个字符，登录成功后会跳转到*个人主页*，用户登录后注册按钮会消失，如果需要注册新的账号请在*个人主页*登出后重新注册。

虽然您不登录也可以使用本网站的一些功能，但本网站的核心功能（模型和数据集的上传与模型测试）均只有在您登录后才能使用，因此如果您想尽情畅享本网站的各种功能，那就赶紧来注册一个账号吧！

### 上传模型

您可以在*个人主页*里选择上传模型，进入*上传模型页面*后需要**选择您上传模型的类型**并**填写模型名称和描述**，模型名称**不能与其他模型的名称重复**，描述不能超过**1000**个字符。模型描述中请您**详细说明模型的输入输出类型**。 模型现在支持.h5类型的文件（如使用keras中 `save_model`方法生成的文件），如果上传keras训练的模型请您提交**一个.h5的模型文件**即可；我们同样支持pytorch训练的模型文件，如果上传pytorch训练的模型文件则需要提交**两个文件**： 一个是**训练的模型结构(.py)**文件，一个是**参数包(.tar)**文件， 如果不按照要求上传文件**将无法正确测评**！上传成功之后会自动跳转到*模型主页*，失败则会返回*提示页面*。

### 上传数据集

您可以在对应模型的*测试模型页面*点击上传一个本地数据集。数据集支持**.npy类型**文件（numpy专用的二进制文件），需要包含**测试数据**和**标准输出结果**。此外您还可以选择填写datagit的链接来进行上传（对应接口请详阅datagit的使用说明）。 数据集描述请说明**数据集的基本信息和特点**以及**该数据集针对哪个模型（请您务必按照模型描述的格式上传数据集文件，否则将无法正常测评！）**。

需要额外说明的是，出于版权和一些其他因素考量，我们**暂不支持用户下载其他用户上传的数据集**，目前所有数据集只能在本平台上使用，模型同理，因此请您**不要试图将本平台当做免费网盘用于存放文件**！

### 测试模型

您在*模型主页*选择测试模型，然后在输入框中输入您想要测试的数据集**全名**，所有的数据集信息可以在*数据集展示页面*看到（当然也可以通过*搜索页面*进行搜索）。点击测试按钮，请耐心等待，如果测试成功会跳转到*测试结果页面*，显示本次测试的准确率和测试用例个数。

### 其他页面

我们支持对模型和数据集的搜索，用户可以点击搜索按钮进入*搜索页面*，在对应的搜索框中输入模型（或数据集）的名称即可进行搜索。我们的搜索方式是**基于子串查找**，因此请您在搜索时输入**相对准确的名称**！

在*搜索结果页面*（包括*模型展示页面*）点击模型可以到达*模型主页*，我们在模型主页上展示了该模型的所有测试历史，用户可以根据该模型的测试历史查找到对应的测试数据集。

同样，在*模型主页*我们还提供了对模型进行修改（可以修改名称和描述）以及对模型进行删除的功能，但这些功能仅限**您为模型上传者登录后**方能使用

此外，在*模型主页*我们还提供了到达模型上传者*个人主页*的链接，您可以点击链接到达该模型的上传者查看他上传的其他模型和数据集以及他对模型进行测试的历史。

您也可以在**登录后**点击右上角的用户名进入自己的*个人主页*，在自己的个人主页上不仅可以查看上述信息，还可以对自己的个人信息（用户名、密码）进行修改（需要提供**正确的密码**），此外还可以进行模型的上传。

我们在首页上展示了一些模型和数据集，如果想要查看本网站所有的模型或数据集您可以点击*模型*或*数据集*进行查看。

## 其他

### 说明与鸣谢

本项目是课程项目，在实现过程中难免有大量的不足与疏漏，给您使用带来的不便敬请谅解！

本项目在实现过程中得到了课程老师与助教的大量帮助，在此对一直为我们提供指导和资源支持的老师和助教们表示深深的感谢！

### 联系我们

在本网站使用过程中遇到什么问题，您可以使用包括但不限于大喊大叫、念念有词、自言自语、哭天抢地等方式尝试联系我们，但我们多半不会接收到您的联系，而且由于课程结束我们我们大概率不会对这一项目提供进一步的支持，因此即使您联系到了我们也没什么用，当然我们同样认为不会有人使用我们的网站，因此这一部分其实是公告撰写者的恶趣味。
